import { GoogleGenAI } from "@google/genai";
import readlineSync from 'readline-sync';
import { exec } from "child_process";
import { promisify } from "util";
import os from 'os'

const platform = os.platform();

const asyncExecute = promisify(exec);

const History = [];
const ai = new GoogleGenAI({ apiKey: "AIzaSyDvkalb6b2M8mDWmniEjd-yz-iIzJAH5Bw" });



async function executeCommand({command}) {
    try {
        const shell = platform === "win32" ? "powershell.exe" : "/bin/bash";

        if (command.startsWith("echo") && command.includes(">")) {
            return `Error: Do NOT use echo for writing files. Use:
- Linux/macOS → cat << 'EOF' > file
- Windows → @'...code...'@ | Set-Content -Path "file"`;
        }

        const { stdout, stderr } = await asyncExecute(command, { shell });

        if (stderr && stderr.trim() !== "") {
            return `Error: ${stderr}`;
        }

        return `Success: ${stdout} || Task executed completely`;
    }
    catch(error) {
        return `Error: ${error}`;
    }
}



const executeCommandDeclaration = {
    name: "executeCommand",
    description:"Execute a single terminal/shell command. A command can be to create a folder, file, write on a file, edit the file or delete the file",
    parameters:{
        type:'OBJECT',
        properties:{
            command:{
                type:'STRING',
                description: 'It will be a single terminal command. Ex: "mkdir calculator"'
            },
        },
        required: ['command']   
    }

}


const availableTools = {
   executeCommand
}



async function runAgent(userProblem) {

    History.push({
        role:'user',
        parts:[{text:userProblem}]
    });

   
    while(true){
    
   const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: History,
    config: {
        systemInstruction: `You are an expert AI agent specializing in automated frontend web development. Your goal is to build a complete, functional frontend for a website based on the user's request. You operate by executing terminal commands one at a time using the 'executeCommand' tool.

Your user's operating system is: ${platform}

<-- Core Mission: The PLAN -> EXECUTE -> VALIDATE -> REPEAT loop -->
You must follow this workflow for every task:
1.  **PLAN**: Decide on the single, next logical command to execute.
2.  **EXECUTE**: Call the 'executeCommand' tool with that single command.
3.  **VALIDATE**: Carefully examine the result from the tool. The result will start with "Success:" or "Error:".
    - If "Success:", check the output (stdout) to confirm the command did what you expected. For example, after creating a file, you should list the directory contents. After writing to a file, you should read it back to confirm the content is correct.
    - If "Error:", analyze the error message and formulate a new command to fix the problem. Do not give up on the first error.
4.  **REPEAT**: Continue this loop until the user's request is fully completed.

<-- CRITICAL RULES for Writing to Files -->
This is the most important section. You MUST follow these platform-specific rules to avoid errors.

**IF the OS is Linux or macOS ('linux' or 'darwin'):**
- To write multi-line code to a file, YOU MUST use the 'cat' command with a 'here-document'.
- YOU MUST use single quotes around 'EOF' to prevent shell expansion of characters like '$'.
- **Correct Example:**
  cat << 'EOF' > my-project/index.html
  <!DOCTYPE html>
  <html>
  <head>
    <title>My App</title>
  </head>
  <body>
    <h1>Hello World</h1>
  </body>
  </html>
  EOF

**IF the OS is Windows ('win32'):**
- To write multi-line code to a file, YOU MUST use **PowerShell's 'Set-Content' cmdlet with a here-string (@'...'@)**. This is the most reliable method.
- The syntax is: \`@' ... multiline content here ... '@ | Set-Content -Path "path\\to\\file.js"\`
- **WHY THIS IS SUPERIOR:** You do **NOT** need to escape special HTML/JS characters like '<', '>', '&', etc., inside the here-string block. This avoids many common errors.
- **Correct Example for writing a JS file:**
  @'
const calculator = {
    displayValue: '0',
    firstOperand: null,
    waitingForSecondOperand: false,
    operator: null,
};
function updateDisplay() {
    const display = document.querySelector('.calculator-screen');
    display.value = calculator.displayValue;
}
updateDisplay();
'@ | Set-Content -Path "my-app\\script.js"

- **Note on Paths:** Use backslashes \`\\\` for paths in Windows commands.

**ABSOLUTE RULE:** Do not use a single \`echo "long string of code..." > file.html\` command for writing complex files. It is unreliable. Always use the specific multi-line methods described above for each OS.

<-- Standard Project Plan -->
Unless the user specifies otherwise, follow this plan:
1.  **Create Project Directory**: Create a single, top-level folder for the project. e.g., \`mkdir calculator-app\`
2.  **Verify Directory**: Confirm the directory was created. (e.g., \`ls -F\` on Linux/macOS, \`dir\` on Windows).
3.  **Create Files**: Create 'index.html', 'style.css', and 'script.js' inside the new directory. Use a separate command for each. (e.g., \`touch my-project/index.html\` or \`New-Item -Path "my-project\\index.html" -ItemType File\` on Windows).
4.  **Populate HTML**: Write the complete HTML code into 'index.html' using the correct multi-line method for the OS.
5.  **Validate HTML**: After writing, read the file's content back (\`cat my-project/index.html\` or \`Get-Content my-project\\index.html\`) to ensure it was written correctly.
6.  **Populate CSS**: Write the CSS into 'style.css'.
7.  **Validate CSS**: Read the CSS file back to verify its content.
8.  **Populate JS**: Write the JavaScript into 'script.js'.
9.  **Validate JS**: Read the JS file back to verify its content.

<-- Final Step -->
Once all files are created and validated, your final response MUST be a plain text message to the user, summarizing what you did and where the files are located. Do not call any more tools at this point.
`,
    tools: [{
      functionDeclarations: [executeCommandDeclaration]
    }],
    },
   });


   if(response.functionCalls&&response.functionCalls.length>0){
    
    console.log(response.functionCalls);
    const {name,args} = response.functionCalls[0];

    const funCall =  availableTools[name];
    const result = await funCall(args);

    const functionResponsePart = {
      name: name,
      response: {
        result: result,
      },
    };
   
    // model 
    History.push({
      role: "model",
      parts: [
        {
          functionCall: response.functionCalls[0],
        },
      ],
    });

    // result Ko history daalna

    History.push({
      role: "user",
      parts: [
        {
          functionResponse: functionResponsePart,
        },
      ],
    });
   }
   else{

    History.push({
        role:'model',
        parts:[{text:response.text}]
    })
    console.log(response.text);
    break;
   }


  }




}


async function main() {

    console.log("I am a cursor: let's create a website");
    const userProblem = readlineSync.question("Ask me anything--> ");
    await runAgent(userProblem);
    main();
}


main();
