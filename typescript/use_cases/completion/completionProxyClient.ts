import * as path from "path";
import * as dotenv from "dotenv";
import * as readline from "readline";
import { Command, Option } from "commander";
import OpenAI from "openai";
import { Completion } from "openai/resources/completions";

interface IProgramOptions {
  stream: boolean;
  cacheControl: ("no-cache" | "no-store")[];
}

const envFilePath = path.resolve(__dirname, "../../.env.sample");
dotenv.config({ path: envFilePath });

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const PROXY_HOST = process.env.PROXY_HOST;
const RAG_BUDDY_TOKEN = process.env.RAG_BUDDY_TOKEN;
const OPENAI_VERSION = process.env.OPENAI_VERSION;

const baseURL = `${PROXY_HOST}/proxy/sem/${OPENAI_VERSION}`;

async function testCompletionAsyncStream(
  prompt: string,
  cacheControl: string[]
) {
  // Pass the cache control header, if provided
  let cacheControlHeader = {};
  if (cacheControl.length) {
    cacheControlHeader = {
      "Helvia-RAG-Buddy-Cache-Control": cacheControl.join(", "),
    };
  }

  const headers = {
    "Helvia-RAG-Buddy-Token": RAG_BUDDY_TOKEN,
    ...cacheControlHeader,
  };

  const client = new OpenAI({
    apiKey: OPENAI_API_KEY,
    baseURL,
    defaultHeaders: headers,
    timeout: 10000,
  });

  const { data: stream, response } = await client.completions
    .create({
      prompt,
      model: "gpt-3.5-turbo-instruct",
      stream: true,
    })
    .withResponse();

  const chunks: Completion[] = [];
  let completionText = "";
  console.log("\n");
  // Iterate through the stream, if it breaks, the test failed
  for await (const chunk of stream) {
    chunks.push(chunk);
    if (chunk.choices[0].finish_reason) {
      break;
    }
    const chunkText = chunk.choices[0].text || "";
    if (chunkText) {
      console.log(chunkText);
      completionText += chunkText;
    }
  }

  console.log("\n", response.headers);

  if (response.headers.has("Helvia-RAG-Buddy-Cache-Status")) {
    const status = response.headers.get("Helvia-RAG-Buddy-Cache-Status");
    const cacheHit = !!(status && status !== "null");
    console.log(`\nCache hit: ${cacheHit}`);
  }
}

async function testCompletionAsync(prompt: string, cacheControl: string[]) {
  // Pass the cache control header, if provided
  let cacheControlHeader = {};
  if (cacheControl.length) {
    cacheControlHeader = {
      "Helvia-RAG-Buddy-Cache-Control": cacheControl.join(", "),
    };
  }

  const headers = {
    "Helvia-RAG-Buddy-Token": RAG_BUDDY_TOKEN,
    ...cacheControlHeader,
  };

  const client = new OpenAI({
    apiKey: OPENAI_API_KEY,
    baseURL,
    defaultHeaders: headers,
    timeout: 10000,
  });

  const response = await client.completions
    .create({
      prompt,
      model: "gpt-3.5-turbo-instruct",
    })
    .asResponse();

  const data = await response.json();

  console.log("\n", data.choices[0].text);
  console.log("\n", "Model: ", data.model);
  console.log("\n", "Headers: ", response.headers);

  if (response.headers.has("Helvia-RAG-Buddy-Cache-Status")) {
    const status = response.headers.get("Helvia-RAG-Buddy-Cache-Status");
    const cacheHit = !!(status && status !== "null");
    console.log(`\nCache hit: ${cacheHit}`);
  }
}

function main() {
  const program = new Command();

  program
    .description("Process a prompt for completion.")
    .option("--stream", "Enable streaming completion", false)
    .addOption(
      new Option(
        "--cache-control <values...>",
        "Set SemCache cache-control header"
      )
        .default([])
        .choices(["no-cache", "no-store"])
    )
    .parse(process.argv);

  const options: IProgramOptions = program.opts();

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  rl.question("Please enter the prompt you want to complete: ", (prompt) => {
    rl.close();
    options.stream
      ? testCompletionAsyncStream(prompt, options.cacheControl)
      : testCompletionAsync(prompt, options.cacheControl);
  });
}

main();
