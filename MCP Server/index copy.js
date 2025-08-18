import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "Weather Data Fetcher",
  version: "1.0.0",
});

async function getWeatherByCity(city = "") {
  if (city.toLowerCase() === "kolkata") {
    return { temp: "30C", forecast: "chances of rain" };
  }
  return { temp: "N/A", forecast: "Data not available" };
}

server.tool(
  "getWeatherDataByCityName",
  {
    city: z.string(),
  },
  async ({ city }) => {
    const data = await getWeatherByCity(city);
    return {
      content: [
        {
          type: "text",
          text: `Weather in ${city}: Temp ${data.temp}, Forecast: ${data.forecast}`,
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
server.connect(transport);
