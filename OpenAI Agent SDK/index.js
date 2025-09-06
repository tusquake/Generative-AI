import axios from "axios";
import { tool, Agent, run } from "some-ai-sdk";
import { z } from "zod";

const getWeatherInfoByCityTool = tool({
  name: "get_weather",
  description: "Get Weather Info by City Name",
  parameters: z.object({
    city: z.string().describe("City name"),
  }),
  async execute({ city }) {
    console.log(`Fetching weather for ${city}`);
    const url = `https://wttr.in/${city.toLowerCase()}?format=%t`;
    const result = await axios.get(url, { responseType: "text" });
    console.log(`Got the response for ${city}: ${result.data}`);
    return result.data;
  },
});

const customerSupportAgent = new Agent({
  name: "Customer Support Agent",
  tools: [getWeatherInfoByCityTool],
  instructions: `
    You are an expert customer support agent which helps users in answering their query
  `,
});

async function main(query = "") {
  const varOcg = await run(customerSupportAgent, query);
  console.log("Final Result:", varOcg.finalOutput);
}

main("What is the weather in New York?");
