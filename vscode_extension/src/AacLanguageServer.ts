import * as fs from "fs";
import { ExtensionContext, Hover, HoverProvider, languages, ProviderResult, window, workspace } from "vscode";
import { LanguageClient, LanguageClientOptions, ServerOptions, Trace } from "vscode-languageclient/node";
import { execShell } from "./AacTaskProvider";
import { ensureTrue, getConfigurationItem } from "./helpers";

const MIN_REQUIRED_PYTHON_VERSION = "3.9";
const DEFAULT_LSP_SERVER_HOST = "127.0.0.1";
const DEFAULT_LSP_SERVER_PORT = 8080;

export class AacLanguageServerClient {
    private static instance: AacLanguageServerClient;

    private aacLspClient!: LanguageClient;

    private constructor() { }

    public static makeLspClient(): AacLanguageServerClient {
        if (!AacLanguageServerClient.instance) {
            AacLanguageServerClient.instance = new AacLanguageServerClient();
        }
        return AacLanguageServerClient.instance;
    }

    public startLanguageServer(context: ExtensionContext): void {
        this.ensureAacToolIsAvailable();
        this.ensureLspServerIsReady(context);
    }

    public shutdownServer(): void {
        this.aacLspClient.stop();
    }

    private ensureAacToolIsAvailable(): void {
        const pythonPath = this.getConfigurationItemFile("pythonPath");
        this.ensureCorrectPythonVersionIsInstalled(pythonPath);
        this.ensureCorrectAacVersionIsInstalled(pythonPath);
    }

    private getConfigurationItemFile(name: string): string {
        const item: string = getConfigurationItem(name);
        ensureTrue(item.length > 0, `Cannot start Language Server; '${item}' is not configured!`);
        ensureTrue(fs.existsSync(item), `Cannot use ${item} as it does not exist!`);
        return item;
    }

    private async ensureCorrectPythonVersionIsInstalled(pythonPath: string): Promise<void> {
        const resolve = await execShell(`${pythonPath} --version`, {});
        ensureTrue(!resolve.stderr, `Could not get the Python version.\n${resolve.stderr}`);

        const pythonVersion = resolve.stdout.match(/\d+\.\d+\.\d+/)?.pop() ?? "unknown";
        ensureTrue(
            pythonVersion.startsWith(MIN_REQUIRED_PYTHON_VERSION),
            `The AaC tool requires Python ${MIN_REQUIRED_PYTHON_VERSION} or newer; current version is: ${pythonVersion}`,
        );
    }

    private async ensureCorrectAacVersionIsInstalled(pythonPath: string): Promise<void> {
        const resolve = await execShell(`${pythonPath} -m pip freeze`);
        ensureTrue(!resolve.stderr, `Could not get the installed AaC version.\n${resolve.stderr}`);

        const expectedAacVersion: string = getConfigurationItem("version") ?? "";
        const aacVersionPattern = new RegExp(`aac==${expectedAacVersion}|-e git.*egg=aac`, "ig");
        const actualAacVersion = resolve.stdout.match(aacVersionPattern)?.pop();
        ensureTrue(!!actualAacVersion, `The installed aac version is ${actualAacVersion} which is unsupported.`);
    }

    private ensureLspServerIsReady(context: ExtensionContext): void {
        const aacPath: string = this.getConfigurationItemFile("aacPath");
        this.startLspClient(
            context,
            aacPath,
            getConfigurationItem("lspServerHost") ?? DEFAULT_LSP_SERVER_HOST,
            getConfigurationItem("lspServerPort") ?? DEFAULT_LSP_SERVER_PORT,
        );
    }

    private startLspClient(context: ExtensionContext, aacPath: string, host: string, port: number): void {
        if (this.aacLspClient) { return; }
        this.aacLspClient = new LanguageClient(
            "aac",
            "AaC Language Client",
            this.getServerOptions(aacPath, "start-lsp", "--host", host, "--port", `${port}`),
            this.getClientOptions(),
        );
        this.aacLspClient.trace = Trace.Verbose;
        context.subscriptions.push(this.aacLspClient.start());
        this.registerHoverProvider(context);
    }

    private async registerHoverProvider(context: ExtensionContext): Promise<void> {
        const client = this.aacLspClient;
        context.subscriptions.push(languages.registerHoverProvider({ scheme: "file", language: "aac", pattern: "**/*.yaml" }, {
            provideHover(document, position, token): ProviderResult<Hover> {
                window.showInformationMessage(
                    `File: ${document.uri.path}; Line: ${position.line}; Character: ${position.character}`
                );
                return client.sendRequest("textDocument/hover", {
                    textDocument: document,
                    position: position,
                }, token);
            }
        }));
    }

    private getServerOptions(command: string, ...args: any[]): ServerOptions {
        return {
            args,
            command,
        };
    }

    private getClientOptions(): LanguageClientOptions {
        return {
            documentSelector: [
                { scheme: "file", language: "aac", pattern: "**/*.aac" },
                { scheme: "file", language: "aac", pattern: "**/*.yaml" },
            ],
            diagnosticCollectionName: "aac",
            outputChannelName: "Architecture-as-Code",
            synchronize: {
                fileEvents: workspace.createFileSystemWatcher("**/.clientrc"),
            }
        };
    }

}