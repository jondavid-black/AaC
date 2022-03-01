import { execShell } from "./helpers";
import { getOutputChannel } from "./outputChannel";
import { window, QuickPickOptions, InputBoxOptions, OpenDialogOptions, Uri } from 'vscode';

const outputChannel = getOutputChannel();

interface CommandArgument {
    name: string;
    description: string;
    userResponse?: string;
}

/**
 * Prompts the user for input then executes the AaC plugin with user-provided
 * information and arguments.
 */
 export async function executeAacCommand(): Promise<void> {

    let availableCommands: string[] = await getAacCommandNames();

    const quickPickOptions: QuickPickOptions = {
        canPickMany: false,
    };

    window.showQuickPick(availableCommands, quickPickOptions).then(commandName => {
        if(commandName) {
            getAacCommandArgs(commandName).then(async (commandArguments) => {
                await getCommandArgUserInput(commandArguments);
                execAacShellCommand(commandName, commandArguments).then(output => {
                    outputChannel.appendLine(output);
                    outputChannel.show();
                });
            });
        }
    });
}

/**
 * Gets the version of the currently installed AaC package
 * @returns string of the version number or null if not installed.
 */
export async function getAaCVersion(): Promise<string|null> {

    let aacVersionOutput: string = "";
    try {
        aacVersionOutput = await execAacShellCommand("version");
    } catch (exception) {
        // TODO: Change to logging or alternative
    }

    const regExp = /([0-9]+\.*){3}/;
    const versionMatch = regExp.exec(aacVersionOutput);
    return versionMatch ? versionMatch[0] : null;
}

async function getCommandArgUserInput(commandArguments: CommandArgument[]) {

    let unansweredCommandArguments: CommandArgument[] = commandArguments.filter(argument => { return (argument.userResponse === undefined); } );

    if (unansweredCommandArguments.length > 0) {
        let argumentToPromptFor = unansweredCommandArguments[0];
        const dialogBoxOptions: OpenDialogOptions = {
            title: argumentToPromptFor.name,
            canSelectMany: false
        };
        const inputBoxOptions: InputBoxOptions = {
            title: argumentToPromptFor.name,
            prompt: argumentToPromptFor.description,
        };

        if (argumentToPromptFor.description.toLowerCase().includes("path")){
            let fileUri: Uri[] | undefined = await window.showOpenDialog(dialogBoxOptions);
            argumentToPromptFor.userResponse = fileUri ? fileUri[0]?.path : "";

        } else {
            argumentToPromptFor.userResponse = await window.showInputBox(inputBoxOptions);
        }
    } else if(unansweredCommandArguments.length > 1) {
        getCommandArgUserInput(commandArguments);
    }
}

async function getAacCommandNames(): Promise<string[]> {
    const aacHelpOutput = await execAacShellCommand("-h");
    return parseTaskNamesFromHelpCommand(aacHelpOutput);
}

/**
 * @returns list of Command arguments
 */
async function getAacCommandArgs(aacCommandName: string): Promise<CommandArgument[]> {
    const aacHelpOutput = await execAacShellCommand(`${aacCommandName} -h`);
    return parseTaskArgsFromHelpCommand(aacHelpOutput);
}

/**
 * Executes AaC commands with arguments.
 * @param command - AaC command name
 * @param commandArgs - command arguments and
 * @returns
 */
async function execAacShellCommand(command: string, commandArgs: CommandArgument[] = []): Promise<string> {

    let commandArgsArray = ["aac", command, ...(commandArgs.map(argument => argument.userResponse))];
    try {
        const { stdout, stderr } = await execShell(commandArgsArray.join(" "), {});
        const stringOutput = stderr.length > 0 ? stderr : stdout;
        return stringOutput;
    } catch (error: any) {
        let errorMessage = error.stderr || error.stdout || "urecognized error";

        outputChannel.appendLine(`Failed to execute AaC command:\n${errorMessage}`);
        outputChannel.show(true);
        throw error;
    }
}

/**
 * Parses command names from the AaC help message.
 * @param aacHelpOutput - the output to parse
 * @returns array of available command names
 */
function parseTaskNamesFromHelpCommand(aacHelpOutput: string): string[] {

    const regExp = /{(.*?)}/;
    const commandNamesMatch = regExp.exec(aacHelpOutput);

    let commandNames: string[] = [];
    if (commandNamesMatch && commandNamesMatch.length >= 2) {
        commandNames = commandNamesMatch[1].split(",");
    }

    return commandNames;
}

/**
 * Parses argument names and descriptions from command help output
 * @param aacHelpOutput - the output to parse
 * @returns array of CommandArgument objects
 */
function parseTaskArgsFromHelpCommand(aacHelpOutput: string): CommandArgument[] {

    const regExp = /^  (?<argName>\S+)\s+(?<argDescription>.*)$/gm;
    const commandArgumentsMatch = regExp.exec(aacHelpOutput);

    let commandArguments: CommandArgument[] = [];
    if (commandArgumentsMatch) {
        commandArguments.push({
            name: commandArgumentsMatch.groups?.argName ?? "<argument name>",
            description: commandArgumentsMatch.groups?.argDescription ?? "<argument description>"
        });
    }

    return commandArguments;
}