import argparse
import commands

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subParsers = parser.add_subparsers(dest="command")

    addpaser = subParsers.add_parser("add")
    addpaser.add_argument("--description", nargs='?', help="Expense Description")
    addpaser.add_argument("--amount", type=float, required=True, help="Expense Amount")
    addpaser.add_argument("--category", help="Expense Category")

    subParsers.add_parser("list")

    summaryparser = subParsers.add_parser("summary")
    summaryparser.add_argument("--month", type=int, help="Month Number (1-12)")
    summaryparser.add_argument("--budget", type=float, help="Optional Monthly Budget")

    deleteparser = subParsers.add_parser("delete")
    deleteparser.add_argument("--id", type=int, required=True, help="Expense ID")

    updateParser = subParsers.add_parser("update")
    updateParser.add_argument("--id", type=int, required=True, help="Expense ID")
    updateParser.add_argument("--description", nargs='?', help="New Description")
    updateParser.add_argument("--amount", type=float, help="New Amount")
    updateParser.add_argument("--category", help="New category")

    subParsers.add_parser("export")

    args = parser.parse_args()
    if args.command == "add":
        commands.addExpense(args.description, args.amount,  args.category)
    elif args.command == "list":
        commands.listExpenses()
    elif args.command == "summary":
        commands.expensesSummary(args.month, args.budget)
    elif args.command == "delete":
        commands.deleteExpense(args.id)
    elif args.command == "update":
        commands.updateExpenses(args.id, args.description, args.amount, args.category)
    elif args.command == "export":
        commands.exportToCsv()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()