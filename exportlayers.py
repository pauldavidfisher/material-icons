#!/usr/bin/python2
import codecs
import sys
import os
from xml.dom import minidom

LAYER_KEY = 'inkscape:groupmode'
LAYER_VAL = 'layer'
LABEL_KEY = 'inkscape:label'
STYLE_KEY = 'style'

def usage():
    print '''
Usage: exportlayers.py <input.svg> <output-dir>

Exports all Inkscape layers from the given <input.svg> into separate SVG files within
the <output-dir> directory.

Layers with labels starting with _ will never be exported. Files are named after the
layer names. Existing files will NOT be overwritten.
'''.strip()

def get_layers(src):
    """
    Returns all layers in the given SVG that don't start with an underscore

    :param src: The source SVG to load
    :return:
    """
    layers = []
    svg = minidom.parse(open(src))
    for g in svg.getElementsByTagName('g'):
        if (
            g.hasAttribute(LAYER_KEY) and
            g.getAttribute(LAYER_KEY) == LAYER_VAL and
            g.hasAttribute(LABEL_KEY) and
            g.getAttribute(LABEL_KEY)[:1] != '_'
        ):
            layers.append(g.attributes[LABEL_KEY].value)
    return layers

def export_layer(layer, src, dst):
    """
    Exports a single layer and makes it visible

    :param layer: The name of the layer to export
    :param src: The source SVG to load
    :param dst: The destination SVG to write to
    :return:
    """
    svg = minidom.parse(open(src))

    for g in svg.getElementsByTagName('g'):
        if (
            g.hasAttribute(LAYER_KEY) and
            g.getAttribute(LAYER_KEY) == LAYER_VAL and
            g.hasAttribute(LABEL_KEY)
        ):
            if g.getAttribute(LABEL_KEY) != layer:
                # not the layer we want - remove
                g.parentNode.removeChild(g)
            elif g.hasAttribute(STYLE_KEY):
                # make sure the layer isn't hidden
                style = g.getAttribute(STYLE_KEY)
                style = style.replace('display:none', '')
                g.setAttribute(STYLE_KEY, style)

    export = svg.toxml()
    codecs.open(dst, "w", encoding="utf8").write(export)


def main():
    """
    Handle commandline arguments and run the tool
    :return:
    """
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    infile = sys.argv[1]
    if not os.path.isfile(infile):
        print "Can't find %s" % infile
        sys.exit(1)

    outdir = sys.argv[2]
    if not os.path.isdir(outdir):
        print "%s seems not to be a directory" % outdir
        sys.exit(1)

    layers = get_layers(infile)
    print "found %d suitable layers" % len(layers)

    for layer in layers:
        outfile = "%s.svg" % os.path.join(outdir, layer)
        if(os.path.isfile(outfile)):
            print "%s - %s exists, skipped" % (layer, outfile)
            continue
        else:
            export_layer(layer, infile, outfile)
            print "%s - %s exported" % (layer, outfile)

    sys.exit(0)


if __name__ == "__main__":
    main()


