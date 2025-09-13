import express from "express";
import fetch from "node-fetch";
import bodyParser from "body-parser";
import cors from "cors";

const app = express();
const PORT = 3000;
const api_key = "sk-V1OY3e6zpJtEowje4Ro8LDChLq19Rm7iJ8mAnQCAJhaKigrH";

app.use(cors());
app.use(bodyParser.json());

app.post("/generate", async (req, res) => {
  const { prompt } = req.body;
  if (!prompt) return res.status(400).json({ error: "Prompt required" });

  try {
    const response = await fetch("https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": `Bearer ${api_key}`
      },
      body: JSON.stringify({
        text_prompts: [{ text: prompt }],
        cfg_scale: 7,
        steps: 30,
        width: 1024,
        height: 1024
      })
    });

    if (!response.ok) {
      const err = await response.text();
      return res.status(500).send(err);
    }

    const data = await response.json();
    if (!data.artifacts) return res.status(500).json({ error: "No artifacts found" });

    res.json({ image: data.artifacts[0].base64 });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Something went wrong" });
  }
});

app.listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
