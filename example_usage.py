from client import MVCCEngine

def main():
    mvcc = MVCCEngine()
    tx1 = mvcc.begin_transaction()
    mvcc.write(tx1, "account", 500)
    tx2 = mvcc.begin_transaction()
    tx3 = mvcc.begin_transaction()
    mvcc.write(tx3, "account", 1200)

    print("MVCC Snapshot Isolation Verification:")
    print(f"Tx2 (snapshot) reads: {mvcc.read(tx2, 'account')} (Expected: 500)")
    print(f"Tx3 (current) reads: {mvcc.read(tx3, 'account')} (Expected: 1200)")

if __name__ == "__main__":
    main()
