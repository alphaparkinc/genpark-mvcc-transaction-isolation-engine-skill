import sys
import json
from client import MVCCEngine

mvcc = MVCCEngine()

def handle_rpc(line):
    global mvcc
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-mvcc-transaction-isolation-engine-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "begin_tx",
                    "description": "Begin a new MVCC transaction with unique timestamp/snapshot ID",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "write_tx",
                    "description": "Write a versioned value under a transaction ID",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "tx_id": {"type": "integer"},
                            "key": {"type": "string"},
                            "value": {"type": "string"}
                        },
                        "required": ["tx_id", "key", "value"]
                    }
                },
                {
                    "name": "read_tx",
                    "description": "Read a value under snapshot isolation rules for a transaction ID",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "tx_id": {"type": "integer"},
                            "key": {"type": "string"}
                        },
                        "required": ["tx_id", "key"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "begin_tx":
            tx_id = mvcc.begin_transaction()
            res = {"content": [{"type": "text", "text": json.dumps({"tx_id": tx_id})}]}
        elif tool_name == "write_tx":
            mvcc.write(args.get("tx_id"), args.get("key"), args.get("value"))
            res = {"content": [{"type": "text", "text": json.dumps({"status": "written"})}]}
        elif tool_name == "read_tx":
            val = mvcc.read(args.get("tx_id"), args.get("key"))
            res = {"content": [{"type": "text", "text": json.dumps({"value": val})}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
