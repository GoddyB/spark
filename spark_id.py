"""``_preimage`` is the normative serializer. The id is the last 16 lowercase
hex characters of SHA-256 over the UTF-8 of that JSON object. The stored id
is not an input. Strings are not trimmed and not Unicode-normalized.
"""

import hashlib
import json
import re
import sys
from collections.abc import Iterable
from pathlib import Path

_ID_RE = re.compile(r"^[0-9a-f]{16}$")


class SparkId:
    """16 lowercase hexadecimal characters. Callers do not build this."""

    __slots__ = ("_hex",)

    def __init__(self) -> None:
        raise TypeError("SparkId cannot be constructed by callers")

    def __str__(self) -> str:
        return self._hex

    def __eq__(self, other: object) -> bool:
        """Not equal to str."""
        if not isinstance(other, SparkId):
            return NotImplemented
        return self._hex == other._hex

    def __hash__(self) -> int:
        return hash(self._hex)


def _spark_id(hex_digits: str) -> SparkId:
    if not isinstance(hex_digits, str) or _ID_RE.fullmatch(hex_digits) is None:
        raise SparkFileError("id must be 16 lowercase hex characters")
    sid = object.__new__(SparkId)
    sid._hex = hex_digits
    return sid


class SparkFileError(Exception):
    """A file or a connect input broke the format or the id rule."""


class Spark:
    """One SPARK record. question and answer are exact code points. id is derived."""

    __slots__ = ("_question", "_answer", "_id")

    def __init__(self) -> None:
        raise TypeError("use Spark.create")

    @classmethod
    def create(cls, question: str, answer: str) -> Spark:
        """Return the Spark for these exact strings.

        A lone surrogate has no UTF-8 preimage and raises SparkFileError.
        """
        if not isinstance(question, str) or not isinstance(answer, str):
            raise TypeError("question and answer must be str")
        try:
            digest = hashlib.sha256(_preimage(question, answer)).hexdigest()
        except UnicodeEncodeError as exc:
            raise SparkFileError("preimage is not UTF-8") from exc
        spark = object.__new__(cls)
        spark._question = question
        spark._answer = answer
        spark._id = _spark_id(digest[-16:])
        return spark

    @property
    def question(self) -> str:
        return self._question

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def id(self) -> SparkId:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Spark):
            return NotImplemented
        return (
            self._question == other._question
            and self._answer == other._answer
            and self._id == other._id
        )

    def __hash__(self) -> int:
        return hash((self._question, self._answer, self._id))


def _preimage(question: str, answer: str) -> bytes:
    return json.dumps(
        {"answer": answer, "question": question, "type": "SPARK"},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def load(path: Path) -> tuple[Spark, ...]:
    """Read one spark.json file into Sparks, in array order.

    Does not search parent or child directories and does not write.
    An empty array returns (). JSON errors, OS errors, shape errors,
    and SparkFileError from create raise SparkFileError.
    Does not return a partial tuple.
    """
    if not isinstance(path, Path):
        raise TypeError("path must be pathlib.Path")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise SparkFileError(exc.strerror or "cannot read file") from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SparkFileError("file is not UTF-8") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SparkFileError(f"invalid JSON: {exc.msg}") from exc
    if not isinstance(data, list):
        raise SparkFileError("expected a JSON array")
    found: list[Spark] = []
    seen: set[SparkId] = set()
    for item in data:
        if not isinstance(item, dict) or set(item) != {
            "type",
            "question",
            "answer",
            "id",
        }:
            raise SparkFileError(
                "each record must be an object with keys type, question, answer, and id"
            )
        wire_type = item["type"]
        question = item["question"]
        answer = item["answer"]
        stored = item["id"]
        if (
            wire_type != "SPARK"
            or not isinstance(question, str)
            or not isinstance(answer, str)
            or not isinstance(stored, str)
            or _ID_RE.fullmatch(stored) is None
        ):
            raise SparkFileError(
                "type must be SPARK, question and answer must be strings, and id must be 16 lowercase hex characters"
            )
        built = Spark.create(question, answer)
        if str(built.id) != stored:
            raise SparkFileError("stored id does not match the record")
        if built.id in seen:
            raise SparkFileError("duplicate id")
        seen.add(built.id)
        found.append(built)
    return tuple(found)


def connect(*groups: Iterable[Spark]) -> tuple[Spark, ...]:
    """Set-union by id of Sparks that are already loaded.

    Walks groups in argument order, then each Spark in iteration order.
    The first Spark for an id is kept. A later Spark with that id and the
    same question and answer is skipped. A later Spark with that id and a
    different question or answer raises SparkFileError. Does not return a
    partial tuple. A non-Spark raises TypeError.

    Does not read the filesystem and does not rehash.
    connect(connect(a, b), a) == connect(a, b) when a and b do not conflict.
    """
    first: dict[SparkId, Spark] = {}
    ordered: list[Spark] = []
    for group in groups:
        for spark in group:
            if not isinstance(spark, Spark):
                raise TypeError("connect expects Spark values")
            kept = first.get(spark.id)
            if kept is None:
                first[spark.id] = spark
                ordered.append(spark)
                continue
            if kept.question != spark.question or kept.answer != spark.answer:
                raise SparkFileError("same id with a different question or answer")
    return tuple(ordered)


def main(argv: list[str]) -> int:
    """Check one file with load. No flags and no subcommands.

    argv must be the program and one path. Otherwise write the usage line
    to stderr and return 1. On success write nothing and return 0. On
    SparkFileError write ``spark_id: <path>: <message>`` and return 1.
    """
    if len(argv) != 2:
        sys.stderr.write("spark_id: usage: python3 spark_id.py <spark.json>\n")
        return 1
    path = argv[1]
    try:
        load(Path(path))
    except SparkFileError as exc:
        sys.stderr.write(f"spark_id: {path}: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
