#!/usr/bin/env python
import os
import sys
import json
import pprint


def fn_join(glue, elements):
    return glue.join(elements)


def fn_split(glue, string):
    return string.split(glue)


def fn_env(name, default):
    return os.environ.get(name, default)


def fn_select(index, array):
    return array[index]


def fn_bool(value):
    return bool(value)


def fn_int(value):
    return int(value)


def get_function_by_name(name):
    return {
        "Fn::Join": fn_join,
        "Fn::Split": fn_split,
        "Fn::Env": fn_env,
        "Fn::Select": fn_select,
        "Fn::Int": fn_int,
        "Fn::Bool": fn_bool
    }[name]


def apply(name, *args):
    return get_function_by_name(name)(*args)


def is_intrinsic_function_object(object_):
    if not isinstance(object_, dict):
        return False

    if object_.keys()[0].startswith("Fn::"):
        return True

    return False


def evaluate(data):
    name = data.keys()[0]
    args = data.values()[0]

    args = parse_this(args)

    return apply(name, *args)


def parse_this(object_):
    if is_intrinsic_function_object(object_):
        return evaluate(object_)

    if isinstance(object_, dict):
        return {k: parse_this(v) for k, v in object_.iteritems()}
    elif isinstance(object_, list):
        return map(parse_this, object_)
    elif isinstance(object_, basestring):
        return object_
    elif isinstance(object_, int):
        return object_

    raise NotImplementedError("ZEE WHAT!? %s" % object_.__class__.__name__)


def parse(path):
    with open(path, "rb") as f:
        data = json.load(f)

    data = parse_this(data)

    print json.dumps(data, indent=2)


if __name__ == "__main__":
    parse(sys.argv[1])
