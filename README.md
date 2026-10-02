# Spark

Spark is a way of gathering, maintaining, and structuring context about a project in Q&A pairs. Any directory can have a spark.json file. Each object in spark.json has: a "type" value of "SPARK", a "question" value, an "answer" value, and a unique ID which is a short hash — the last N characters of the object's byte hash — used to connect Sparks idempotently regardless of origin machine, directory, etc. Anywhere in the directory or at the root level, a Spark binary can be placed (its features will be defined later); it gathers meaningful insights using the GraphQL-like database that this way of connecting Sparks allows.

This repository scaffolds that file format. The Spark binary's features are not implemented here. There is no GraphQL engine. The notes below are format choices so an id is computable. They are not extra product claims.

## Format choices

N is 16. The hash is SHA-256. The characters are lowercase hexadecimal. The id is the last 16 of those characters.

The hashed bytes are the UTF-8 text of one JSON object with the keys answer, question, and type. type is SPARK. The stored id is not one of those bytes. Keys are in alphabetical order, with no extra whitespace. `spark_id.py` is that serializer. Strings are not trimmed. Strings are not Unicode-normalized. The same question and answer on any machine produce the same id.

Recompute the id in `spark.json` with this command.

```bash
python3 -c 'import hashlib,json; q="What is Spark?"; a="Spark is a way of gathering, maintaining, and structuring context about a project in Q&A pairs."; p=json.dumps({"answer":a,"question":q,"type":"SPARK"},ensure_ascii=False,sort_keys=True,separators=(",",":")).encode(); print(hashlib.sha256(p).hexdigest()[-16:])'
```

The command prints `107ee97d1abd8e36`.

Check a file with `python3 spark_id.py spark.json`. Exit code 0 and no output means every stored id matches the rule. `spark.schema.json` checks the shape of the array. It does not restate the hash.

## How ids connect

Equal ids are the same Spark, whatever the machine or the directory. `connect` in `spark_id.py` unions records that are already loaded. It does not read a directory and it is not a query. Array order is not identity. The same id with the same question and answer is one Spark. The same id with a different question or answer is an error.

## The binary

`bin/spark` is a placeholder. It exits 0, writes nothing, and has no features. A later Spark binary may sit in a directory or at that directory's root. This repository does not define what that binary does.

`SKILL.md` is an agent skill that also uses the name SPARK. That file is not a spark.json record. Its five headings are not fields on a Spark. This scaffold does not change `SKILL.md`.
