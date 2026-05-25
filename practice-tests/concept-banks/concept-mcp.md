# MCP & Tool Design — Question Bank

## Question 1
MCP is often described as "the USB-C for AI integrations." What does this metaphor capture about the protocol?

A) MCP is a hardware standard that devices must physically connect through, similar to how USB-C works in electronics
B) MCP provides a universal, standardized interface that replaces custom one-off integrations, allowing an AI application to connect with any MCP-compatible tool or data source through the same protocol
C) MCP was designed by the same standards organization that created the USB-C specification, ensuring hardware-level compatibility between AI devices
D) MCP is the fastest protocol for AI data transfer, just as USB-C offers the highest data throughput among physical connectors

<details>
<summary>Answer</summary>

**B)** MCP is a software protocol layer that replaces the N×M combinatorial problem of custom point-to-point integrations — just as USB-C replaced a drawer full of proprietary cables with a single universal connector. A is wrong because MCP is a software protocol, not a hardware standard, and there is no physical connector or device requirement in the spec. C is wrong because MCP is an Anthropic-led open protocol, not a product of any USB standards body. D is wrong because throughput is not MCP's differentiator — standardized discovery, lifecycle management, and capability negotiation are. (source: MCP integration)

</details>

---

## Question 2
What is the primary problem that the Model Context Protocol (MCP) solves in the AI ecosystem?

A) Reducing the cost of LLM API calls by compressing prompt data before transmission over the network
B) Providing a standard protocol for AI models to securely access external tools, data sources, and context without requiring custom integration code for each connection
C) Standardizing model weight formats so that different LLM vendors can share parameter data across training pipelines
D) Replacing the need for fine-tuning by allowing models to dynamically load capabilities through protocol extensions

<details>
<summary>Answer</summary>

**B)** MCP eliminates the N×M integration problem by providing a single standard protocol for tool discovery, capability negotiation, and execution — any MCP host connects to any MCP server without bespoke glue code. A is wrong because MCP does not compress or optimize prompt data; it is a connection and capability protocol, not a compression layer. C is wrong because MCP has nothing to do with model weight formats or cross-vendor training pipelines. D is wrong because MCP does not replace fine-tuning; it expands runtime access to external context and tools without changing model weights. (source: MCP integration)

</details>

---

## Question 3
In MCP architecture, there are three key roles: Host, Client, and Server. Which statement correctly describes their relationships?

A) The Host application creates one Client per MCP server, and each Client maintains a 1:1 connection with exactly one Server
B) The Host acts as a central load balancer, distributing requests across a pool of Clients which then fan out to any available Server in the cluster
C) The Client is embedded within the Server process, and the Host connects directly to the Server through the Client's local API
D) Multiple Hosts share a single Client instance which multiplexes connections to all configured Servers simultaneously

<details>
<summary>Answer</summary>

**A)** In the MCP architecture the Host (e.g., Claude Desktop) owns and creates one Client per configured Server, with each Client maintaining a strict 1:1 transport connection to exactly one Server — this isolation prevents one server's failures or behavior from affecting another's connection. B is wrong because MCP has no load-balancer or fan-out concept; each Client connects to exactly one Server, not a pool. C is wrong because Clients live inside the Host process, not inside the Server process — the Server is a separate entity that the Client connects to. D is wrong because Clients are not shared across Hosts; each Host owns its own set of dedicated Clients. (source: MCP integration)

</details>

---

## Question 4
A developer is integrating MCP into a custom chat application. Their app needs to connect to three different MCP servers: a filesystem server, a database server, and a weather API server. How many MCP clients should the host application create?

A) One client that connects to all three servers through a single multiplexed transport connection
B) Three clients — one for each server — because every MCP client maintains a 1:1 connection with exactly one server
C) One client per active user session, with the client dynamically routing requests to the appropriate server based on the tool being called
D) The number depends on the transport type — stdio servers can share one client, but HTTP servers each require their own dedicated client

<details>
<summary>Answer</summary>

**B)** The MCP spec mandates a 1:1 Client-to-Server relationship regardless of transport type — three servers means three clients, each with its own dedicated transport connection and initialization handshake. A is wrong because MCP has no multiplexing concept at the client layer; each client manages exactly one server connection, not a shared channel to multiple servers. C is wrong because clients are created per server at configuration time, not per user session, and routing is the Host's responsibility, not a client-level concern. D is wrong because the 1:1 rule applies equally to stdio and Streamable HTTP — the transport type does not change client cardinality. (source: MCP integration)

</details>

---

## Question 5
An MCP server exposes an `execute_sql_query` capability. The model decides when to call it, provides SQL parameters, and the server runs the query and returns results. Which MCP primitive does this represent?

A) A Resource — because the capability provides access to database data that the model reads at application-controlled times
B) A Prompt — because the server is injecting the query results as templated context into the model's conversation
C) A Tool — because it represents a model-controlled, executable function that the model invokes with parameters and receives dynamic, computed results
D) A Notification — because the server pushes query results to the model whenever database changes occur

<details>
<summary>Answer</summary>

**C)** Tools are the MCP primitive for model-controlled, executable functions — the model decides when to invoke them, supplies parameters, and receives dynamic computed results, which matches exactly how `execute_sql_query` behaves. A is wrong because Resources are application-controlled and read-only; the application (not the model) decides which resource to expose, and the data is not computed on demand with model-supplied parameters. B is wrong because Prompts are server-defined, user-selectable templates that are chosen before the model runs, not dynamically invoked functions that the model calls mid-conversation. D is wrong because Notifications are one-way signals from server to client about state changes; they do not carry query results and are not a primitive the model invokes. (source: Tool use)

</details>

---

## Question 6
Your application lets users browse a file tree. When a user clicks a file, you want the AI model to be able to read its contents. Which MCP primitive should you expose for this?

A) A Tool named `read_file` — because reading a file is an action that the model must actively execute by calling a function
B) A Resource — because the file's contents are application-controlled, read-only data that the application decides to expose, and the model accesses them without choosing which specific file to read
C) A Prompt template with a `{fileContent}` placeholder — so the file content is always injected as conversation context before the model responds
D) A Capability declaration — because file reading is an implicit server capability that the client must negotiate during initialization

<details>
<summary>Answer</summary>

**B)** Resources represent application-controlled, read-only data — the user click (not the model) triggers the selection, the application decides which file to expose, and the model accesses its content as provided context, matching the Resource primitive exactly. A is wrong because a Tool would make the model responsible for deciding which file to read and when — that control belongs to the user and application here, not the model. C is wrong because a Prompt template is a server-defined template the user selects before the conversation; it is not the right primitive for exposing dynamic file content selected at runtime by a user action. D is wrong because Capability declarations are part of the initialization handshake between client and server and do not represent data or actions accessible during a session. (source: MCP integration)

</details>

---

## Question 7
A developer defines conversation starters like "Summarize this meeting" and "Draft an email response" that include dynamic information from the current context. Which MCP primitive best fits this use case?

A) Tools — because each conversation starter triggers a specific server-side function to generate a response
B) Resources — because conversation starters are static text blocks served as read-only data from the server
C) Prompts — because they are server-defined, user-selectable templates that include dynamic context and are explicitly chosen by the user before being sent to the model
D) Sampling requests — because the server needs to generate completions from the model based on the conversation starter text

<details>
<summary>Answer</summary>

**C)** Prompts are the MCP primitive for server-defined, user-selectable templates that can include dynamic context injected at selection time — exactly what "Summarize this meeting" and "Draft an email response" are. A is wrong because Tools are model-invoked functions for executing actions; conversation starters are user-selected templates, not functions the model decides to call. B is wrong because Resources are application-controlled data blobs accessed as read-only context; they are not templates that structure how the user starts a conversation. D is wrong because Sampling requests are how MCP servers ask the host/model to generate a completion on the server's behalf — the opposite direction of what a conversation starter needs. (source: MCP integration)

</details>

---

## Question 8
What is the Host application's primary responsibility regarding MCP clients?

A) The Host directly encodes and decodes JSON-RPC messages for all server communication, bypassing the client layer entirely
B) The Host manages the lifecycle of multiple clients, creates one client per configured server, and orchestrates which client receives which user intent based on the current conversation
C) The Host serves as a reverse proxy, forwarding MCP messages from the AI model to remote servers and caching responses for subsequent requests
D) The Host introspects each server's source code to generate appropriate tool definitions, eliminating the need for servers to self-describe

<details>
<summary>Answer</summary>

**B)** The Host owns the user experience and is responsible for reading server configurations, creating and destroying Clients (one per configured Server), and deciding which Client should handle a given user request — Clients handle the actual transport and protocol mechanics. A is wrong because JSON-RPC encoding is the Client's responsibility; the Host operates at a higher orchestration level and does not bypass the Client layer. C is wrong because the Host is not a reverse proxy or caching layer — it creates discrete Clients that each own their own direct connection to a single Server. D is wrong because Servers self-describe their tools via `tools/list` during the session; the Host never reads server source code. (source: MCP integration)

</details>

---

## Question 9
An MCP host application crashes while clients are mid-conversation with their respective servers. When the host process restarts, what happens to the client-server connections?

A) All connections automatically resume — MCP servers maintain persistent state independently of the host process lifecycle
B) All previous client-server connections are terminated, and the host must create new clients and re-initialize each server connection from scratch
C) Only Streamable HTTP connections survive the crash; stdio-based connections are permanently lost and cannot be recovered
D) Each server caches its session state and restores the conversation context when the host reconnects, preserving tool call history

<details>
<summary>Answer</summary>

**B)** MCP Clients live inside the Host process — when the Host crashes, every Client and its associated transport connection is destroyed simultaneously, and the Host must re-create every Client, re-establish every transport, and complete the full initialization handshake for each Server from scratch on restart. A is wrong because MCP servers do not maintain independent persistent state tied to a disconnected client; session state is tied to the active transport connection, which is gone when the Host crashes. C is wrong because both stdio and Streamable HTTP connections are managed by Client objects inside the Host process — both are lost when the Host crashes; there is no transport-specific survival rule. D is wrong because MCP specifies no server-side session caching or reconnection protocol; servers do not restore conversation context for a new connection. (source: MCP integration)

</details>

---

## Question 10
A developer is building a local-first MCP server for static code analysis. The server runs as a subprocess and should communicate without any network stack. Which transport should they use?

A) Streamable HTTP on localhost — because it still avoids remote network configuration while providing the same API surface
B) stdio — because it communicates over standard input/output streams of a subprocess, requires zero network configuration, and involves no ports or TLS
C) WebSocket transport — because it enables persistent bidirectional communication between the host process and the server process
D) Unix domain sockets — because they are the standard inter-process communication mechanism defined by the MCP specification

<details>
<summary>Answer</summary>

**B)** stdio transport communicates exclusively over the stdin/stdout streams of a locally spawned subprocess — it requires no ports, no TLS certificates, and no network stack at all, making it the perfect fit for a local-first subprocess server. A is wrong because even localhost HTTP still requires binding a TCP port and initializing a network stack, violating the "without any network stack" requirement. C is wrong because WebSockets require an HTTP upgrade handshake and a TCP port, which is a network stack dependency; additionally, WebSockets are not a standard MCP transport defined in the spec. D is wrong because Unix domain sockets are not a transport type defined by the MCP specification — only stdio and Streamable HTTP are standard MCP transports. (source: MCP integration)

</details>

---

## Question 11
A team wants to deploy their MCP server as a cloud service so remote users can access it. The server also needs to authenticate incoming connections. Which transport should they use?

A) stdio transport with SSH tunneling — because the SSH layer provides both remote access and authentication without changing the MCP transport
B) Streamable HTTP transport — because it operates over standard HTTP(S), supports bearer token and other HTTP authentication mechanisms, and is designed for remote MCP server access
C) Both stdio and Streamable HTTP simultaneously — stdio for local sessions and HTTP for remote sessions, with automatic transport failover
D) gRPC transport — because MCP's protocol buffer layer enables authentication middleware that stdio and HTTP lack

<details>
<summary>Answer</summary>

**B)** Streamable HTTP is the MCP transport designed for remote deployment — it operates over standard HTTPS, supports bearer tokens and other HTTP authentication headers natively, and can be hosted as a standard cloud service behind a load balancer or API gateway. A is wrong because stdio is inherently a local subprocess transport that communicates via stdin/stdout; SSH tunneling is an external wrapper, not a change to the MCP transport, and the underlying stdio transport still cannot accept independent remote connections. C is wrong because an MCP server exposes one transport per connection endpoint, not simultaneous dual-transport with failover; that is not a concept in the MCP specification. D is wrong because gRPC is not a transport defined by the MCP specification — only stdio and Streamable HTTP are standard MCP transports. (source: MCP integration)

</details>

---

## Question 12
A developer deploys a local MCP server using stdio transport and tests it successfully. They then try to access that same server from a different machine on the same network and it fails. What is the reason?

A) stdio transport communicates through stdin/stdout of a local subprocess — it has no network interface, no listening port, and cannot accept connections from any remote machine
B) The MCP protocol mandates TLS encryption for all cross-machine communication, and stdio does not support TLS certificate configuration
C) stdio transport only works on Linux because Windows and macOS handle subprocess standard streams differently at the operating system level
D) Remote access over stdio is disabled by default and requires explicitly setting the `"allowRemote": true` flag in the MCP server configuration

<details>
<summary>Answer</summary>

**A)** stdio transport is architected around subprocess stdin/stdout streams — there is no socket, no listening port, and no network interface involved, so the server is physically incapable of receiving a connection from any machine other than the one that spawned the subprocess. B is wrong because the failure is not about TLS — stdio never reaches the network layer at all; TLS configuration is irrelevant when there is no network socket to encrypt. C is wrong because stdio transport works on Linux, macOS, and Windows; all modern operating systems provide subprocess standard streams, and the MCP spec makes no OS-specific exclusions. D is wrong because there is no `allowRemote` configuration flag in the MCP specification; stdio transport has no remote access mode at all, regardless of configuration. (source: MCP integration)

</details>

---

## Question 13
What is the correct sequence when an MCP client first establishes a connection with a server?

A) The client sends `tools/list` immediately, the server responds with available tools, and the connection is implicitly established with that first exchange
B) The client sends an `initialize` request carrying its capabilities and protocol version, the server responds with its own capabilities, then the client sends `notifications/initialized` — only after this handshake can the client list and call tools
C) The server sends a `greeting` notification upon connection, the client acknowledges it with a `ready` message, then the server pushes its complete tool and resource definitions to the client
D) The client opens the transport, the server immediately begins streaming available tools and resources through server-initiated messages, and no explicit initialization step is required

<details>
<summary>Answer</summary>

**B)** The MCP initialization lifecycle is strictly sequenced: client sends `initialize` with its protocol version and capabilities, server responds with its own capabilities, client confirms with `notifications/initialized`, and only then can either side exchange `tools/list`, `resources/list`, or tool calls — requests sent before this handshake completes are rejected by spec. A is wrong because sending `tools/list` before `initialize` violates the MCP lifecycle; the server must reject requests from an uninitialized connection. C is wrong because there is no `greeting` notification or `ready` message in the MCP specification; the server does not push capabilities — the client must request them. D is wrong because MCP requires an explicit initialization handshake before any capability exchange; servers do not spontaneously stream tool definitions on connection. (source: MCP integration)

</details>

---

## Question 14
During MCP initialization, a client declares support for the "roots" capability. The server does not support this capability. What is the outcome?

A) The server rejects the connection — capability mismatches are fatal initialization errors in the MCP handshake
B) The server ignores the unsupported capability and establishes the connection normally — only capabilities that both sides support are active for the session
C) The server attempts to implement roots support dynamically by loading a plugin that matches the capability declaration
D) The client automatically downgrades its protocol version to match the server's narrower capability set before retrying

<details>
<summary>Answer</summary>

**B)** MCP capability negotiation is additive and non-destructive — the effective capability set for a session is the intersection of what both sides declared, and any capability declared by only one party is simply inactive; the connection proceeds normally. A is wrong because the MCP spec explicitly does not treat capability mismatches as fatal errors; unrecognized capabilities are silently ignored by the party that does not support them. C is wrong because MCP has no dynamic plugin loading mechanism for capability fulfillment; server capabilities are fixed at startup, not dynamically acquired during handshake. D is wrong because the client does not retry with a downgraded protocol version due to capability mismatches; protocol version negotiation and capability negotiation are separate concerns, and capability differences do not trigger a version downgrade. (source: MCP integration)

</details>

---

## Question 15
After the initialization handshake completes successfully, an MCP client needs to discover what tools the server provides. Which request should it send?

A) `tools/discover` — a standard MCP method that returns all available tool metadata including names, descriptions, and parameter schemas
B) `tools/list` — which returns an array of tool definitions, each with a name, description, and JSON Schema input schema describing expected parameters
C) `server/describe` — a unified method that returns the complete server manifest including tools, resources, and prompts in a single response
D) `capabilities/query` — because tool discovery is part of the capability negotiation phase and must be completed before tools can be called

<details>
<summary>Answer</summary>

**B)** `tools/list` is the MCP-specified method for tool discovery post-initialization — it returns an array of tool objects each containing a name, description, and JSON Schema `inputSchema` that the client and model use to understand how to call the tool. A is wrong because `tools/discover` does not exist in the MCP specification; the correct method name is `tools/list`. C is wrong because `server/describe` does not exist in the MCP specification; tools, resources, and prompts are discovered through separate `tools/list`, `resources/list`, and `prompts/list` requests, not a unified manifest call. D is wrong because `capabilities/query` does not exist in the MCP specification; capability negotiation happens during `initialize`, not as a separate discovery request after initialization. (source: MCP integration)

</details>

---

## Question 16
What format does MCP use for encoding all messages — requests, responses, and errors — exchanged between clients and servers?

A) Protocol Buffers (protobuf) — because MCP needs efficient binary encoding with strict schema validation for large tool call results
B) JSON-RPC 2.0 — a lightweight remote procedure call protocol that uses JSON for structured request/response messaging with standardized error codes
C) GraphQL — because MCP needs flexible queries that let clients request only the specific tool fields they need without over-fetching data
D) MessagePack — a compact binary serialization format that MCP uses to minimize transport overhead for high-throughput tool calls

<details>
<summary>Answer</summary>

**B)** MCP builds on JSON-RPC 2.0 for all message encoding — requests carry `method`, `params`, and `id`; responses carry `result`; errors carry a standardized `code`, `message`, and optional `data` — the same protocol foundation used by the Language Server Protocol. A is wrong because MCP uses human-readable JSON, not binary Protocol Buffers; the spec makes no use of protobuf schemas or binary wire encoding. C is wrong because GraphQL is a query language for APIs with its own schema and resolver model; MCP uses simple JSON-RPC method calls, not GraphQL queries or mutations. D is wrong because MessagePack is a binary serialization format not used by MCP; all MCP messages are valid JSON text, not compact binary. (source: MCP integration)

</details>

---

## Question 17
An MCP client specifies protocol version "2024-11-05" during initialization. The server supports version "2025-03-26" but not "2024-11-05" directly. What happens?

A) The connection succeeds — the server responds with its own version and operates in a mode compatible with the client's declared version
B) The server forces the client to upgrade by responding with an error that includes the minimum supported protocol version
C) The connection is rejected because the protocol version must match exactly — MCP does not support version negotiation across different dates
D) The client automatically probes for compatibility by retrying the initialize request with progressively newer version strings until the server accepts one

<details>
<summary>Answer</summary>

**A)** MCP protocol versioning is designed for forward compatibility — servers respond with their own supported version and adapt their behavior to remain compatible with older clients; the connection succeeds as long as the server can interoperate with the declared client version. B is wrong because the MCP spec does not define an error-based upgrade flow; servers do not respond with an error demanding a version upgrade during normal version negotiation. C is wrong because MCP explicitly does not require exact version matching — the protocol is designed to be forward-evolvable with older clients able to connect to newer servers. D is wrong because the MCP spec defines no automatic retry-with-probe behavior; the client sends its version once in `initialize` and the server handles compatibility. (source: MCP integration)

</details>

---

## Question 18
A developer's MCP stdio server writes debug log messages to stdout between JSON-RPC responses. Why does this break communication with the client?

A) stdout is the transport channel for JSON-RPC messages in stdio mode — any non-JSON output intermixed with protocol messages corrupts the message stream, and the client cannot parse the combined output as valid JSON-RPC
B) stdout output is subject to operating system rate limits, and excessive log messages exhaust the I/O quota needed for actual MCP protocol responses
C) The MCP client interprets every line written to stdout as a tool call result, causing phantom tool executions that produce incorrect conversation state
D) stdout is reserved for MCP protocol-level heartbeat pings, and debugging output interferes with the keep-alive timing mechanism

<details>
<summary>Answer</summary>

**A)** In stdio transport, stdout is the exclusive channel for JSON-RPC messages — the client reads stdout and attempts to parse every byte as JSON-RPC; any non-JSON debug text interleaved between protocol messages produces unparseable output and breaks the framing, causing the client to fail. All server-side logging must go to stderr, which is separate from the MCP transport channel. B is wrong because operating systems do not impose I/O rate limits on stdout in a way that would affect MCP; the problem is parsing corruption, not bandwidth exhaustion. C is wrong because the client does not interpret arbitrary stdout lines as tool call results — it expects valid JSON-RPC message structure; malformed bytes produce parse errors, not phantom tool executions. D is wrong because MCP stdio transport has no heartbeat or keep-alive mechanism; stdout carries JSON-RPC request/response messages only, not protocol-level pings. (source: MCP integration)

</details>

---

## Question 19
A developer needs to inspect the JSON-RPC messages being exchanged between their MCP client and a Streamable HTTP server during development. Which tool should they use?

A) The MCP Inspector — a dedicated debugging proxy that sits between client and server, displaying every JSON-RPC request and response with formatted views and allowing interactive testing of individual messages
B) Chrome DevTools Network tab — because Streamable HTTP operates over standard HTTP, all MCP traffic appears as regular HTTP requests in browser developer tools
C) Wireshark — because MCP uses a custom binary framing layer on top of HTTP that requires packet-level protocol analysis
D) The `mcp debug --trace` CLI command built into every MCP SDK that automatically captures and pretty-prints all protocol traffic

<details>
<summary>Answer</summary>

**A)** The MCP Inspector is a purpose-built debugging proxy that understands MCP message semantics — it displays the initialization handshake, capability negotiation, tool definitions, and individual tool call request/response pairs with formatted views and supports interactive testing of messages directly. B is wrong because while Chrome DevTools can show raw HTTP requests, it has no understanding of MCP message semantics, cannot display capability negotiation, and does not provide MCP-aware formatting or interactive tool testing. C is wrong because MCP does not use a custom binary framing layer; all messages are JSON-RPC text over standard HTTP, and Wireshark packet analysis provides far more low-level detail than necessary for MCP debugging. D is wrong because there is no `mcp debug --trace` command built into MCP SDKs; the MCP Inspector is the official debugging tool. (source: MCP integration)

</details>

---

## Question 20
A developer configures an MCP server with a relative path: `./servers/my-mcp-server`. What is this path resolved relative to?

A) The current working directory of the Host application process at the moment the server subprocess is spawned
B) The directory containing the MCP configuration file (such as `claude_desktop_config.json`), regardless of where the Host process was started from
C) The user's home directory — MCP always resolves relative paths starting from `~/` for portability across different system configurations
D) The system's `/usr/local/bin` directory, which is the standard installation location for all MCP server executables

<details>
<summary>Answer</summary>

**A)** Relative paths in MCP configuration are resolved against the Host application's current working directory at the time it spawns the server subprocess — which is why absolute paths are recommended in production to avoid resolution differences between launch environments. B is wrong because the MCP spec does not resolve relative paths relative to the config file's directory; resolution is based on the Host process's working directory, which may differ from where the config file lives. C is wrong because MCP does not canonicalize relative paths against the user's home directory; `~/` expansion is a shell convention, not an MCP path resolution rule. D is wrong because `/usr/local/bin` is a Unix system binary directory with no special significance in MCP path resolution; MCP servers can live anywhere and are found relative to the Host's working directory. (source: Claude Code settings)

</details>

---

## Question 21
A developer's MCP server requires an API key to call a third-party weather service. What is the recommended approach for providing this key to the server at runtime?

A) Hard-code the API key directly in the server's source code so it is always available regardless of how the server is launched
B) Pass the API key through environment variables configured in the `env` field of the MCP server's configuration entry — the Host sets these variables before spawning the server process
C) Embed the API key as a query parameter in the server's connection URL string within the configuration file
D) Send the API key in the `initialize` request as a custom capability so the server can authenticate before serving any tool calls

<details>
<summary>Answer</summary>

**B)** The MCP `env` configuration field lets the Host inject environment variables into the server subprocess before it starts — the actual secret value lives in a `.env` file outside version control, keeping secrets out of both source code and committed configuration. A is wrong because hard-coding secrets in source code violates basic secret hygiene; the key would be exposed in version control and any deployment artifact, and rotation requires a code change. C is wrong because embedding the API key in a connection URL string exposes it in the configuration file, which may be committed to version control, visible in process listings, and logged by the Host. D is wrong because the MCP `initialize` request is for protocol version and capability negotiation, not credential exchange; there is no custom capability mechanism for injecting credentials during handshake. (source: Claude Code settings)

</details>

---

## Question 22
How do MCP Apps fundamentally differ from traditional web applications in their architecture and data flow?

A) MCP Apps run entirely on the server with no client-side rendering, whereas web apps use progressive enhancement for client-side interactivity
B) MCP Apps support bi-directional data flow — both host and server can initiate communication — and they preserve conversation context across interactions, unlike traditional web apps which follow a stateless request-response model
C) MCP Apps compile to WebAssembly for sandboxed client-side execution, while web apps are built with JavaScript and HTML
D) MCP Apps bypass HTTP entirely, using a proprietary WebTransport protocol that reduces latency compared to traditional REST endpoints

<details>
<summary>Answer</summary>

**B)** MCP Apps maintain a stateful, bidirectional connection where servers can push notifications to the host and conversation context persists across tool calls — fundamentally different from the stateless request-response cycle of traditional web apps where each HTTP request is independent. A is wrong because MCP Apps are not about server-side rendering versus client-side rendering; MCP is a protocol layer for AI tool integration, not a web rendering architecture. C is wrong because MCP Apps do not compile to WebAssembly; MCP servers are regular processes communicating over stdio or HTTP, and WebAssembly sandboxing is not part of the MCP specification. D is wrong because MCP uses standard HTTP for Streamable HTTP transport, not a proprietary WebTransport protocol; Streamable HTTP operates over plain HTTPS. (source: MCP integration)

</details>

---

## Question 23
How should an MCP App isolate third-party MCP server code for security?

A) Third-party MCP servers run as separate operating system processes, each with restricted permissions — similar to how mobile platforms sandbox individual apps — providing process-level isolation that prevents a compromised server from accessing the host's or other servers' data
B) All MCP server code runs in the same Node.js event loop with namespace-based isolation, where each server's functions are registered under a unique prefix to prevent collisions
C) Third-party MCP servers execute within sandboxed iframes in the browser, leveraging web platform origin-based security boundaries for isolation
D) The JSON-RPC protocol layer provides built-in sandboxing — each server's methods are automatically scoped to its connection ID without additional process isolation

<details>
<summary>Answer</summary>

**A)** Each MCP server runs as a separate OS process with restricted filesystem access and limited network permissions — process-level boundaries mean a compromised server cannot read the Host's memory, access other servers' data, or escalate privileges beyond its own process space. B is wrong because running all server code in a shared Node.js event loop provides only namespace separation, not security isolation; a malicious server could access shared memory, override globals, or interfere with other servers in the same process. C is wrong because MCP servers are not browser-based and do not execute in iframes; they are standalone processes communicating over stdio or HTTP, and web origin isolation does not apply. D is wrong because JSON-RPC is a message encoding format with no sandboxing capability; connection ID scoping of methods is a routing concern, not a security isolation mechanism — it does nothing to prevent a server from making OS-level calls. (source: MCP integration)

</details>

---

## Question 24
A Python developer sees instructions to run an MCP server using `uv run main.py`. What is `uv` in this context?

A) A testing framework specifically designed for validating MCP server implementations against the protocol specification compliance suite
B) A fast Python package and project manager written in Rust that replaces pip, pip-tools, and virtualenv — `uv run` auto-resolves and installs dependencies before executing the script, similar to how `npx` works for Node.js
C) A virtual environment wrapper that provides isolated Python runtimes but relies on pip for actual package management and resolution
D) A MCP-specific SDK that translates Python type annotations into MCP tool definitions automatically, generating protocol-compliant server scaffolding

<details>
<summary>Answer</summary>

**B)** `uv` is a Rust-based Python package and project manager that replaces pip, pip-tools, virtualenv, and poetry — `uv run` automatically resolves and installs dependencies declared in `pyproject.toml` before executing the script, providing zero-setup execution similar to `npx` for Node.js. A is wrong because `uv` is a general-purpose Python toolchain, not an MCP-specific testing or compliance framework; it has no knowledge of the MCP protocol specification. C is wrong because `uv` does not rely on pip for package resolution; it has its own high-performance dependency resolver written in Rust that is designed to replace pip entirely. D is wrong because `uv` is not an MCP SDK and has no awareness of MCP tool definitions or protocol scaffolding; the MCP Python SDK is a separate library that `uv` can install like any other package. (source: MCP integration)

</details>

---

## Question 25
A developer is building an MCP client using the Python SDK. They need to manage async resources — server connections, transport setup, and session cleanup — ensuring everything is properly closed even if an exception occurs during setup. Which pattern is recommended?

A) Using nested try/finally blocks to explicitly close each resource individually in reverse order of acquisition
B) Using `AsyncExitStack` — a context manager that collects async cleanup callbacks as resources are acquired and ensures every resource is properly closed even when exceptions occur, commonly paired with `connect_to_server` and related context managers
C) Using `atexit.register()` to schedule cleanup callbacks that execute when the Python interpreter process terminates
D) Letting Python's garbage collector handle resource cleanup automatically, since MCP connection objects implement `__del__` finalizers for safe teardown

<details>
<summary>Answer</summary>

**B)** `AsyncExitStack` is the MCP Python SDK's recommended pattern for managing multiple async resources — it dynamically collects cleanup callbacks as each context manager (transport, session, connection) is entered, and guarantees correct reverse-order teardown even when an exception occurs mid-setup. A is wrong because nested try/finally blocks for multiple async resources are error-prone; each additional resource requires another nesting level, and a bug in one finally block can suppress exceptions from others — `AsyncExitStack` handles this correctly by design. C is wrong because `atexit.register()` runs callbacks only when the Python interpreter exits normally; it does not handle exceptions during setup, does not work with async cleanup coroutines, and fires far too late to properly close active network connections. D is wrong because `__del__` finalizers are not guaranteed to run promptly or at all in CPython due to reference cycles, and they cannot await async cleanup coroutines — relying on GC for MCP connection teardown leads to resource leaks. (source: MCP integration)

</details>

---

## Question 26
An MCP server's available tools change at runtime — a new tool is added while clients are connected. How does the server inform connected clients of this change?

A) The server sends a `notifications/tools/list_changed` notification, signaling clients to re-fetch the tool list by sending a new `tools/list` request to get the updated definitions
B) The server pushes the complete updated tool definitions directly in the notification payload, and the client processes the new list without needing a separate re-fetch request
C) The server disconnects all clients and forces a full re-initialization, which causes each client to send a fresh `tools/list` during the new handshake cycle
D) The server embeds the updated tool list as metadata in the response to whichever tool call the client sends next, piggybacking on existing traffic

<details>
<summary>Answer</summary>

**A)** MCP notifications are one-way fire-and-forget signals that carry no data payload — `notifications/tools/list_changed` tells connected clients that the tool list has changed, and each client must then issue a fresh `tools/list` request to retrieve the updated definitions. B is wrong because MCP notifications carry no response expectation and typically contain minimal or no payload; the spec does not define a notification that pushes complete tool definitions — the client must re-fetch via `tools/list`. C is wrong because MCP has no mechanism for a server to force client disconnection and re-initialization in response to tool changes; doing so would disrupt ongoing conversations and is not part of the notification contract. D is wrong because MCP responses carry only the result of the method that was called; there is no piggyback metadata mechanism for injecting updated tool definitions into unrelated tool call responses. (source: MCP integration)

</details>

---

## Question 27
A client receives a `notifications/resources/list_changed` message from an MCP server. Which statement about handling this notification is correct?

A) The client must send an acknowledgment response within five seconds, or the server retransmits the notification assuming it was lost in transit
B) The notification is fire-and-forget with no response expected from the client, but it is only valid if the server declared the corresponding notification capability during initialization
C) The notification payload always includes a complete diff of which resources were added, modified, and removed, so the client can update its cache without a re-fetch
D) The client's MCP SDK automatically re-fetches resources upon receiving this notification — no additional client-side code is required

<details>
<summary>Answer</summary>

**B)** MCP notifications are unidirectional fire-and-forget messages — no acknowledgment is defined in the spec and no retransmission occurs; additionally, a server may only send notification types it declared during the `initialize` handshake, so receiving this notification confirms the server declared that capability. A is wrong because the JSON-RPC 2.0 notification type (no `id` field) explicitly does not expect a response; the MCP spec defines no acknowledgment requirement and no retransmit-on-silence behavior for notifications. C is wrong because `notifications/resources/list_changed` carries no diff payload in the MCP specification; it is a minimal signal that the list changed, and the client must issue a fresh `resources/list` request to learn what changed. D is wrong because the MCP SDK does not automatically re-fetch resources on this notification; the application code must register a handler and explicitly call `resources/list` to retrieve the updated state. (source: MCP integration)

</details>

---

## Question 28
An MCP client calls `tools/call` with parameter `{"file": "report.pdf"}`, but the tool's input schema requires `"filePath"` not `"file"`. The server returns an error with code `-32602`. What does this error code indicate?

A) The server encountered an internal error while executing the tool function — this is a server-side bug in the tool implementation
B) Invalid params — the request parameters do not match the tool's declared input schema, and the error indicates the client sent malformed or incorrectly named parameters
C) The requested tool was not found on the server — the tool may have been removed or renamed since the client last called `tools/list`
D) The request exceeded the server's configured execution timeout — the tool took too long to begin processing the malformed parameters

<details>
<summary>Answer</summary>

**B)** JSON-RPC 2.0 error code `-32602` means "Invalid params" — the server received the request but the parameters `{"file": "report.pdf"}` do not conform to the tool's declared input schema, which requires `filePath`; this is a client-side parameter error indicating the call was structurally malformed. A is wrong because a server-side internal error is signaled by code `-32603` ("Internal error"), not `-32602`; the error here is in the client's parameter structure, not in the tool's execution logic. C is wrong because a missing or unknown method is signaled by code `-32601` ("Method not found"); `-32602` specifically indicates that the method was found but the supplied parameters are invalid. D is wrong because execution timeouts are implementation-specific errors typically reported with application-level error codes above `-32000`, not the standard `-32602` parameter validation code. (source: MCP integration)

</details>

---

## Question 29
A developer is building an MCP client that logs server responses for debugging purposes. Which security practice is most important when implementing this logging?

A) Log every server response at DEBUG level so that developers can always trace the complete data flow for troubleshooting production issues
B) Sanitize or redact sensitive data from server responses before writing to logs — server responses may contain user data, API keys in transit, or proprietary information that should never appear in log files or monitoring systems
C) Disable all logging in production environments entirely — debugging information should only be collected and retained during local development
D) Encrypt each log entry with the originating server's public key so that only the server operator can decrypt and read the debug output

<details>
<summary>Answer</summary>

**B)** MCP tool call results may contain user PII, credentials, or proprietary business data — sanitizing or redacting this before writing to any logging sink prevents sensitive data from appearing in log files, error tracking platforms, and monitoring dashboards where it would be broadly accessible. A is wrong because logging every raw server response at DEBUG level in production creates a data exposure risk; tool results frequently contain user-specific data that should never be stored verbatim in log infrastructure accessible to operations teams. C is wrong because disabling all production logging eliminates the observability needed to detect incidents, diagnose production failures, and audit security events — the solution is selective redaction, not complete logging removal. D is wrong because encrypting logs with the server's public key makes the logs unreadable to the client operator who needs to debug their own system; log encryption, if used, should protect data at rest for the logging system's owner, not make logs inaccessible to the developer. (source: MCP integration)

</details>

---

## Question 30
An MCP client receives a tool call result from a server that does not match the tool's declared output schema — extra fields are present and required fields are missing. What is the safest client-side behavior?

A) Trust the server's output as-is and forward it to the model — the model is designed to handle unstructured and unexpected data gracefully
B) Validate server responses against the declared output schema, and if validation fails, reject the result with a clear error rather than passing potentially malformed or unexpected data to the AI model
C) Silently transform the output to fit the schema by stripping extra fields and inserting default values for any missing required fields
D) Immediately disconnect from the server and permanently blacklist it — any schema mismatch indicates a compromised or malicious server

<details>
<summary>Answer</summary>

**B)** Validating server responses against declared output schemas and surfacing clear errors on mismatch is the correct practice — passing structurally unexpected data to the AI model can cause hallucination, incorrect reasoning, or data leakage that is hard to trace back to the malformed tool result. A is wrong because models are not reliably resilient to structurally malformed inputs; unexpected data shapes can cause the model to misinterpret fields, make incorrect decisions, or produce responses that appear plausible but are based on garbage data. C is wrong because silently transforming output masks real bugs in the server implementation and inserts fabricated values for missing required fields, potentially causing the model to reason on data that was never actually returned by the server. D is wrong because a schema mismatch is more likely a server bug or version skew than a security compromise; immediately disconnecting and blacklisting is a disproportionate response that would cause unnecessary service disruption for what is typically a development-time integration error. (source: MCP integration)

</details>

---
