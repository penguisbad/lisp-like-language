class LStatement {
    args;

    constructor(args) {
        this.args = args;
    }

    execute() {
    }
}
let variables = {};
const getValue = (item) => {
    if (Object.keys(variables).includes(item)) {
        return variables[item];
    }
    if (item instanceof LStatement) {
        return item.execute();
    }
    if (item[0] == '"') {
        return item.substring(1, item.length - 1);
    }
    // check if it is a number
    if (/^\d+$/.test(item)) {
        return parseInt(item);
    }
    if (item == "true") {
        return true;
    }
    if (item == "false") {
        return false;
    }
    alert("Error: " + item + " is not a string, number, or boolean");
}

class LAssignVariable extends LStatement {
    constructor(args) {
        super(args);
    }

    execute() {
        variables[this.args[0]] = getValue(this.args[1]);
    }
}
class LAddition extends LStatement {
    constructor(args) {
        super(args);
    }

    execute() {
        let sum = 0;
        for (let arg of this.args) {
            sum += getValue(arg);
        }
        return sum;
    }
}
class LSubtraction extends LStatement {
    constructor(args) {
        super(args);
    }

    execute() {
        let subtracted = getValue(this.args[0]);
        for (let arg of this.args.slice(1)) {
            subtracted -= getValue(arg);
        }
        return subtracted
    }
}
class LMultiplication extends LStatement {
    constructor(args) {
        super(args);
    }

    execute() {
        let multiplied = 1;
        for (let arg of this.args) {
            multiplied *= getValue(arg);
        }
        return multiplied;
    }
}
class LDivision extends LStatement {
    constructor(args) {
        super(args);
    }
    
    execute() {
        let divided = getValue(this.args[0]);
        for (let arg of this.args.slice(1)) {
            divided /= getValue(arg);
        }
        return divided;
    }
}

class LPrint extends LStatement {
    constructor(args) {
        super(args);
    }

    execute() {
        document.getElementById("output").innerHTML += getValue(this.args[0]);
    }
}
class LPrintLine extends LStatement {
    constructor(args) {
        super(args);
    }

    execute() {
        document.getElementById("output").innerHTML += getValue(this.args[0]) + "<br>";
    }
}

const parse = (text) => {

    let list = [];
    let currentItem = "";
    for (let i = 0; i < text.length; i++) {
        if (text[i] == "(") {
            let counter = 0;
            let ss = "";
            for (let j = i; j < text.length; j++) {
                if (text[j] == "(") {
                    counter++;
                } else if (text[j] == ")") {
                    counter--;
                }
                if (counter == 0) {
                    ss = text.substring(i+1,j);
                    i = j;
                    break;
                }
            }
            currentItem = parse(ss);
            if (i == text.length - 1) {
                list.push(currentItem);
            }
        } else if (text[i] == " " || text[i] == ")" || i == text.length - 1) {
            if (!(currentItem instanceof Array) && i == text.length - 1) {
                currentItem += text[i];
            }
            list.push(currentItem);
            currentItem = "";
        } else {
            currentItem += text[i];
        }
    }
    return list;
}

const parseStatement = (statementList) => {
    let name = statementList[0];
    let args = [];
    for (let i = 1; i < statementList.length; i++) {
        if (statementList[i] instanceof Array) {
            args.push(parseStatement(statementList[i]));
        } else {
            args.push(statementList[i]);
        }
    }
    switch (name) {
        case "print":
            return new LPrint(args);
        case "println":
            return new LPrintLine(args);
        case "+":
            return new LAddition(args);
        case "-":
            return new LSubtraction(args);
        case "*":
            return new LMultiplication(args);
        case "/":
            return new LDivision(args);
        case "assign":
            return new LAssignVariable(args);
        default:
            break;
    }
}

const stringFromArray = (array) => {
    let s = "[";
    for (element of array) {
        if (element instanceof Array) {
            s += stringFromArray(element);
        } else {
            s += element;
        }
        s += ", ";
    }
    return s + "]";
}

const formatText = (text) => {
    let newText = text.replace("<br>", " ");
    return newText.replace(/\s+/g, " ");
}

document.getElementById("run").addEventListener("click", (event) => {
    document.getElementById("output").innerHTML = "";
    let text = document.getElementById("textarea").value;
    let list = parse(formatText(text));
    let statements = [];
    for (let item of list) {
        statements.push(parseStatement(item));
    }
    for (let statement of statements) {
        statement.execute();
    }
});