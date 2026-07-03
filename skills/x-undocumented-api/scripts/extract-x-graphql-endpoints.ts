import { mkdir } from "node:fs/promises";
import { join } from "node:path";

type Operation = {
	operationName: string;
	queryId: string;
	operationType: string;
	sourceScript: string;
	category: string;
};

type ScriptSummary = {
	url: string;
	bytes: number;
	operationCount: number;
	error?: string;
};

type CliOptions = {
	sourcePage: string;
	outDir: string;
	filter: string | null;
};

function usage(): string {
	return [
		"Usage: bun extract-x-graphql-endpoints.ts [--out-dir <dir>] [--source-page <url>] [--filter <regex>]",
		"",
		"Fetches current X client-web bundles and writes:",
		"  x-graphql-endpoints-YYYY-MM-DD.json",
		"  x-graphql-endpoints-YYYY-MM-DD.csv",
		"  x-graphql-community-endpoints-YYYY-MM-DD.md",
		"",
		"Examples:",
		"  bun scripts/extract-x-graphql-endpoints.ts --out-dir /tmp/x-graphql",
		"  bun scripts/extract-x-graphql-endpoints.ts --filter Community --out-dir artifacts",
	].join("\n");
}

function parseArgs(argv: string[]): CliOptions {
	const options: CliOptions = {
		sourcePage: "https://x.com",
		outDir: process.cwd(),
		filter: null,
	};

	for (let index = 0; index < argv.length; index += 1) {
		const arg = argv[index];
		if (arg === "--help" || arg === "-h") {
			console.log(usage());
			process.exit(0);
		}
		if (arg === "--out-dir") {
			options.outDir = requireValue(argv, index, arg);
			index += 1;
			continue;
		}
		if (arg === "--source-page") {
			options.sourcePage = requireValue(argv, index, arg);
			index += 1;
			continue;
		}
		if (arg === "--filter") {
			options.filter = requireValue(argv, index, arg);
			index += 1;
			continue;
		}
		throw new Error(`Unknown argument: ${arg}\n\n${usage()}`);
	}

	return options;
}

function requireValue(argv: string[], index: number, flag: string): string {
	const value = argv[index + 1];
	if (!value || value.startsWith("--")) {
		throw new Error(`${flag} requires a value`);
	}
	return value;
}

function extractScriptUrls(html: string): string[] {
	return Array.from(
		new Set(
			html.match(
				/https:\/\/abs\.twimg\.com\/responsive-web\/client-web\/[^"' <]+?\.js/g,
			) ?? [],
		),
	).sort();
}

function categorize(operationName: string): string {
	if (/communit/i.test(operationName)) return "community";
	if (/search/i.test(operationName)) return "search";
	if (/tweet|post/i.test(operationName)) return "tweet";
	if (/user|profile|followers|following|friendship/i.test(operationName)) {
		return "user";
	}
	if (/list/i.test(operationName)) return "list";
	if (/bookmark/i.test(operationName)) return "bookmark";
	if (/dm|conversation|inbox|chat/i.test(operationName)) return "direct-message";
	if (/notification/i.test(operationName)) return "notification";
	if (/grok/i.test(operationName)) return "grok";
	if (/article/i.test(operationName)) return "article";
	if (/space/i.test(operationName)) return "space";
	if (/commerce|payment|subscription|premium/i.test(operationName)) {
		return "commerce";
	}
	return "other";
}

function extractOperations(source: string, sourceScript: string): Operation[] {
	const operations: Operation[] = [];
	const patterns = [
		{
			regex:
				/queryId:"([^"]+)",operationName:"([^"]+)",operationType:"([^"]+)"/g,
			order: "query-id-first",
		},
		{
			regex:
				/operationName:"([^"]+)",operationType:"([^"]+)",queryId:"([^"]+)"/g,
			order: "operation-name-first",
		},
	] as const;

	for (const pattern of patterns) {
		for (const match of source.matchAll(pattern.regex)) {
			const queryId = pattern.order === "query-id-first" ? match[1] : match[3];
			const operationName =
				pattern.order === "query-id-first" ? match[2] : match[1];
			const operationType =
				pattern.order === "query-id-first" ? match[3] : match[2];
			if (!queryId || !operationName || !operationType) continue;
			operations.push({
				operationName,
				queryId,
				operationType,
				sourceScript,
				category: categorize(operationName),
			});
		}
	}

	return operations;
}

function csvEscape(value: string): string {
	if (!/[",\n]/.test(value)) return value;
	return `"${value.replaceAll('"', '""')}"`;
}

function makeCsv(operations: Operation[]): string {
	return (
		[
			"category,operationType,operationName,queryId,sourceScript",
			...operations.map((op) =>
				[
					op.category,
					op.operationType,
					op.operationName,
					op.queryId,
					op.sourceScript,
				]
					.map(csvEscape)
					.join(","),
			),
		].join("\n") + "\n"
	);
}

function makeCommunityMarkdown(input: {
	generatedAtUtc: string;
	sourcePage: string;
	scriptCount: number;
	totalOperations: number;
	jsonPath: string;
	csvPath: string;
	community: Operation[];
}): string {
	return [
		"# X GraphQL Community Endpoints",
		"",
		`Generated: ${input.generatedAtUtc}`,
		`Source page: ${input.sourcePage}`,
		`Scripts scanned: ${input.scriptCount}`,
		`Total GraphQL operations found: ${input.totalOperations}`,
		`Community operations found: ${input.community.length}`,
		"",
		"Complete operation inventory:",
		`- ${input.jsonPath}`,
		`- ${input.csvPath}`,
		"",
		"## Community Operations",
		"",
		"| Operation | Type | Query ID |",
		"| --- | --- | --- |",
		...input.community.map(
			(op) => `| ${op.operationName} | ${op.operationType} | ${op.queryId} |`,
		),
		"",
	].join("\n");
}

const options = parseArgs(Bun.argv.slice(2));
const filterRegex = options.filter ? new RegExp(options.filter, "i") : null;

const htmlResponse = await fetch(options.sourcePage);
if (!htmlResponse.ok) {
	throw new Error(`Failed fetching ${options.sourcePage}: HTTP ${htmlResponse.status}`);
}

const html = await htmlResponse.text();
const scriptUrls = extractScriptUrls(html);
if (scriptUrls.length === 0) {
	throw new Error(`No X client-web script URLs found in ${options.sourcePage}`);
}

const operationByKey = new Map<string, Operation>();
const sourceScripts: ScriptSummary[] = [];

for (const scriptUrl of scriptUrls) {
	try {
		const response = await fetch(scriptUrl);
		if (!response.ok) {
			sourceScripts.push({
				url: scriptUrl,
				bytes: 0,
				operationCount: 0,
				error: `HTTP ${response.status}`,
			});
			continue;
		}
		const source = await response.text();
		const operations = extractOperations(source, scriptUrl);
		for (const operation of operations) {
			const key = `${operation.operationName}:${operation.queryId}:${operation.operationType}`;
			operationByKey.set(key, operation);
		}
		sourceScripts.push({
			url: scriptUrl,
			bytes: source.length,
			operationCount: operations.length,
		});
	} catch (error) {
		sourceScripts.push({
			url: scriptUrl,
			bytes: 0,
			operationCount: 0,
			error: error instanceof Error ? error.message : String(error),
		});
	}
}

let operations = Array.from(operationByKey.values());
if (filterRegex) {
	operations = operations.filter((op) => filterRegex.test(op.operationName));
}

operations.sort((a, b) => {
	const byCategory = a.category.localeCompare(b.category);
	if (byCategory !== 0) return byCategory;
	const byName = a.operationName.localeCompare(b.operationName);
	if (byName !== 0) return byName;
	return a.queryId.localeCompare(b.queryId);
});

const categoryCounts = operations.reduce<Record<string, number>>((counts, op) => {
	counts[op.category] = (counts[op.category] ?? 0) + 1;
	return counts;
}, {});

const generatedAtUtc = new Date().toISOString();
const date = generatedAtUtc.slice(0, 10);
await mkdir(options.outDir, { recursive: true });

const jsonPath = join(options.outDir, `x-graphql-endpoints-${date}.json`);
const csvPath = join(options.outDir, `x-graphql-endpoints-${date}.csv`);
const communityPath = join(
	options.outDir,
	`x-graphql-community-endpoints-${date}.md`,
);

const payload = {
	generatedAtUtc,
	sourcePage: options.sourcePage,
	filter: options.filter,
	scriptCount: scriptUrls.length,
	sourceScripts,
	totalOperations: operations.length,
	categoryCounts,
	operations,
};

await Bun.write(jsonPath, `${JSON.stringify(payload, null, 2)}\n`);
await Bun.write(csvPath, makeCsv(operations));
await Bun.write(
	communityPath,
	makeCommunityMarkdown({
		generatedAtUtc,
		sourcePage: options.sourcePage,
		scriptCount: scriptUrls.length,
		totalOperations: operations.length,
		jsonPath,
		csvPath,
		community: operations.filter((op) => op.category === "community"),
	}),
);

console.log(
	JSON.stringify(
		{
			generatedAtUtc,
			sourcePage: options.sourcePage,
			filter: options.filter,
			scriptCount: scriptUrls.length,
			totalOperations: operations.length,
			categoryCounts,
			outputs: {
				jsonPath,
				csvPath,
				communityPath,
			},
		},
		null,
		2,
	),
);
