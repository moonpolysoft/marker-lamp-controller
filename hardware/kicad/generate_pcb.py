#!/usr/bin/env python3
"""Generate the two-layer KiCad PCB for the marker-lamp controller.

The generated board intentionally uses oversized SMD pads and conservative
design rules for hand assembly and OSH Park's two-layer process.
"""

from pathlib import Path

import pcbnew


OUT_DIR = Path(__file__).resolve().parent
BOARD_PATH = OUT_DIR / "marker-lamp-controller.kicad_pcb"

MM = pcbnew.FromMM


def point(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


def add_net(board, name):
    net = pcbnew.NETINFO_ITEM(board, name)
    board.Add(net)
    return net


def add_text(fp, text, x, y, layer, size=1.0, thickness=0.15):
    item = pcbnew.PCB_TEXT(fp)
    item.SetText(text)
    item.SetPosition(point(x, y))
    item.SetLayer(layer)
    item.SetTextSize(point(size, size))
    item.SetTextThickness(MM(thickness))
    fp.Add(item)
    return item


def add_pad(
    fp,
    number,
    x,
    y,
    sx,
    sy,
    net,
    *,
    through=False,
    drill=0.0,
    shape=pcbnew.PAD_SHAPE_ROUNDRECT,
):
    pad = pcbnew.PAD(fp)
    pad.SetNumber(str(number))
    pad.SetPosition(point(x, y))
    pad.SetSize(point(sx, sy))
    pad.SetShape(shape)
    if shape == pcbnew.PAD_SHAPE_ROUNDRECT:
        pad.SetRoundRectRadiusRatio(0.18)
    if through:
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetDrillSize(point(drill, drill))
        pad.SetLayerSet(pad.PTHMask())
    else:
        pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        pad.SetLayerSet(pad.SMDMask())
    if net is not None:
        pad.SetNet(net)
    fp.Add(pad)
    return pad


def add_smd_2(
    board,
    ref,
    value,
    x,
    y,
    net1,
    net2,
    *,
    spacing=3.2,
    pad_x=1.5,
    pad_y=1.5,
    body_x=2.2,
    body_y=1.6,
    pin1_right=False,
):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(point(0, 0))
    fp.SetAttributes(pcbnew.FP_SMD)
    left_number, right_number = (2, 1) if pin1_right else (1, 2)
    add_pad(fp, left_number, x - spacing / 2, y, pad_x, pad_y, net1)
    add_pad(fp, right_number, x + spacing / 2, y, pad_x, pad_y, net2)
    rect = pcbnew.PCB_SHAPE(fp)
    rect.SetShape(pcbnew.SHAPE_T_RECT)
    rect.SetStart(point(x - body_x / 2, y - body_y / 2))
    rect.SetEnd(point(x + body_x / 2, y + body_y / 2))
    rect.SetLayer(pcbnew.F_Fab)
    rect.SetWidth(MM(0.15))
    fp.Add(rect)
    add_text(fp, ref, x, y - 2.1, pcbnew.F_Fab, 0.9)
    add_text(fp, value, x, y + 2.1, pcbnew.F_Fab, 0.8)
    board.Add(fp)
    return fp


def add_soic8(board, ref, value, x, y, nets):
    """Hand-solder SO-8 with 1.8 x 0.75 mm exposed copper pads."""
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(point(0, 0))
    fp.SetAttributes(pcbnew.FP_SMD)
    ys = [y - 1.905, y - 0.635, y + 0.635, y + 1.905]
    for idx, py in enumerate(ys, start=1):
        add_pad(fp, idx, x - 3.0, py, 1.8, 0.75, nets[idx])
    for idx, py in zip([8, 7, 6, 5], ys):
        add_pad(fp, idx, x + 3.0, py, 1.8, 0.75, nets[idx])
    body = pcbnew.PCB_SHAPE(fp)
    body.SetShape(pcbnew.SHAPE_T_RECT)
    body.SetStart(point(x - 2.1, y - 2.6))
    body.SetEnd(point(x + 2.1, y + 2.6))
    body.SetLayer(pcbnew.F_Fab)
    body.SetWidth(MM(0.15))
    fp.Add(body)
    pin1 = pcbnew.PCB_SHAPE(fp)
    pin1.SetShape(pcbnew.SHAPE_T_CIRCLE)
    pin1.SetCenter(point(x - 1.45, y - 1.65))
    pin1.SetEnd(point(x - 1.2, y - 1.65))
    pin1.SetLayer(pcbnew.F_Fab)
    pin1.SetWidth(MM(0.15))
    fp.Add(pin1)
    add_text(fp, ref, x, y - 3.5, pcbnew.F_Fab, 0.9)
    add_text(fp, value, x, y + 3.5, pcbnew.F_Fab, 0.8)
    board.Add(fp)
    return fp


def add_opto_smd4(board, ref, value, x, y, nets):
    """Wide DIP-style SMD optocoupler footprint with large gull-wing pads."""
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(point(0, 0))
    fp.SetAttributes(pcbnew.FP_SMD)
    coords = {
        1: (x - 4.5, y - 1.27),
        2: (x - 4.5, y + 1.27),
        3: (x + 4.5, y + 1.27),
        4: (x + 4.5, y - 1.27),
    }
    for num, (px, py) in coords.items():
        add_pad(fp, num, px, py, 2.4, 1.5, nets[num])
    body = pcbnew.PCB_SHAPE(fp)
    body.SetShape(pcbnew.SHAPE_T_RECT)
    body.SetStart(point(x - 3.7, y - 2.5))
    body.SetEnd(point(x + 3.7, y + 2.5))
    body.SetLayer(pcbnew.F_Fab)
    body.SetWidth(MM(0.15))
    fp.Add(body)
    pin1 = pcbnew.PCB_SHAPE(fp)
    pin1.SetShape(pcbnew.SHAPE_T_CIRCLE)
    pin1.SetCenter(point(x - 2.8, y - 1.25))
    pin1.SetEnd(point(x - 2.55, y - 1.25))
    pin1.SetLayer(pcbnew.F_Fab)
    pin1.SetWidth(MM(0.15))
    fp.Add(pin1)
    add_text(fp, ref, x, y - 3.3, pcbnew.F_Fab, 0.9)
    add_text(fp, value, x, y + 3.3, pcbnew.F_Fab, 0.8)
    board.Add(fp)
    return fp


def add_sot23(board, ref, value, x, y, nets):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(point(0, 0))
    fp.SetAttributes(pcbnew.FP_SMD)
    add_pad(fp, 1, x - 1.7, y + 0.95, 1.8, 1.1, nets[1])
    add_pad(fp, 2, x - 1.7, y - 0.95, 1.8, 1.1, nets[2])
    add_pad(fp, 3, x + 1.7, y, 1.8, 1.1, nets[3])
    body = pcbnew.PCB_SHAPE(fp)
    body.SetShape(pcbnew.SHAPE_T_RECT)
    body.SetStart(point(x - 0.9, y - 1.5))
    body.SetEnd(point(x + 0.9, y + 1.5))
    body.SetLayer(pcbnew.F_Fab)
    body.SetWidth(MM(0.15))
    fp.Add(body)
    add_text(fp, ref, x, y - 2.2, pcbnew.F_Fab, 0.9)
    add_text(fp, value, x, y + 2.2, pcbnew.F_Fab, 0.8)
    board.Add(fp)
    return fp


def add_connector(board, nets):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference("J1")
    fp.SetValue("TBP01R1-508-04BE")
    fp.SetPosition(point(0, 0))
    labels = ["SENSE", "BATT+", "LAMP+", "GND"]
    for idx, (net, label) in enumerate(zip(nets, labels), start=1):
        y = 10 + (idx - 1) * 5.08
        shape = pcbnew.PAD_SHAPE_RECT if idx == 1 else pcbnew.PAD_SHAPE_CIRCLE
        add_pad(
            fp,
            idx,
            7,
            y,
            3.2,
            3.2,
            net,
            through=True,
            drill=1.4,
            shape=shape,
        )
        add_text(fp, label, 10.0, y, pcbnew.F_Fab, 0.8)
    outline = pcbnew.PCB_SHAPE(fp)
    outline.SetShape(pcbnew.SHAPE_T_RECT)
    outline.SetStart(point(3.5, 7.2))
    outline.SetEnd(point(12.5, 28.1))
    outline.SetLayer(pcbnew.F_Fab)
    outline.SetWidth(MM(0.2))
    fp.Add(outline)
    add_text(fp, "J1", 7, 5.8, pcbnew.F_Fab, 1.0)
    board.Add(fp)
    return fp


def add_mounting_hole(board, ref, x, y):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue("M3")
    fp.SetPosition(point(0, 0))
    fp.SetAttributes(pcbnew.FP_THROUGH_HOLE)
    pad = pcbnew.PAD(fp)
    pad.SetNumber("")
    pad.SetPosition(point(x, y))
    pad.SetSize(point(6.0, 6.0))
    pad.SetDrillSize(point(3.2, 3.2))
    pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
    pad.SetLayerSet(pad.UnplatedHoleMask())
    fp.Add(pad)
    board.Add(fp)


def add_track(board, net, coords, width=0.35, layer=pcbnew.F_Cu):
    for a, b in zip(coords, coords[1:]):
        tr = pcbnew.PCB_TRACK(board)
        tr.SetStart(point(*a))
        tr.SetEnd(point(*b))
        tr.SetWidth(MM(width))
        tr.SetLayer(layer)
        tr.SetNet(net)
        board.Add(tr)


def add_via(board, net, x, y):
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(point(x, y))
    via.SetWidth(MM(0.8))
    via.SetDrill(MM(0.4))
    via.SetNet(net)
    board.Add(via)


def add_ground_zone(board, net):
    zone = pcbnew.ZONE(board)
    zone.SetLayer(pcbnew.B_Cu)
    zone.SetNet(net)
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in [(1.5, 1.5), (80.5, 1.5), (80.5, 45.5), (1.5, 45.5)]:
        outline.Append(point(x, y))
    board.Add(zone)
    return zone


def build_board():
    board = pcbnew.BOARD()
    board.GetDesignSettings().m_MinClearance = MM(0.20)
    board.GetDesignSettings().m_TrackMinWidth = MM(0.20)
    board.GetDesignSettings().m_ViasMinSize = MM(0.60)
    board.GetDesignSettings().m_ViasMinDrill = MM(0.30)

    nets = {
        name: add_net(board, name)
        for name in [
            "GND",
            "SENSE",
            "SENSE_R1",
            "OPTO_A",
            "VPRE",
            "VPWR",
            "OPTO_C",
            "QBASE",
            "QCOL",
            "CTRL",
            "LAMP_OUT",
        ]
    }

    # 80 x 45 mm outline. Extra room is intentional for hand assembly.
    outline = [(1, 1), (81, 1), (81, 46), (1, 46), (1, 1)]
    for a, b in zip(outline, outline[1:]):
        edge = pcbnew.PCB_SHAPE(board)
        edge.SetShape(pcbnew.SHAPE_T_SEGMENT)
        edge.SetStart(point(*a))
        edge.SetEnd(point(*b))
        edge.SetLayer(pcbnew.Edge_Cuts)
        edge.SetWidth(MM(0.1))
        board.Add(edge)

    add_mounting_hole(board, "H1", 5, 5)
    add_mounting_hole(board, "H2", 77, 5)
    add_mounting_hole(board, "H3", 77, 42)
    add_mounting_hole(board, "H4", 5, 42)

    add_connector(
        board,
        [nets["SENSE"], nets["VPRE"], nets["LAMP_OUT"], nets["GND"]],
    )

    add_smd_2(board, "R1", "1k", 17, 10, nets["SENSE"], nets["SENSE_R1"])
    add_smd_2(board, "R2", "1k", 23, 10, nets["SENSE_R1"], nets["OPTO_A"])
    add_smd_2(
        board,
        "D3",
        "1N4148WS",
        23,
        14,
        nets["GND"],
        nets["OPTO_A"],
        spacing=3.8,
        pad_x=1.7,
        pad_y=1.5,
        pin1_right=True,
    )

    add_opto_smd4(
        board,
        "U2",
        "VO617A-4X017T",
        32,
        11.27,
        {
            1: nets["OPTO_A"],
            2: nets["GND"],
            3: nets["GND"],
            4: nets["OPTO_C"],
        },
    )

    add_smd_2(
        board,
        "D1",
        "STPS2H100A",
        17,
        18,
        nets["VPRE"],
        nets["VPWR"],
        spacing=5.5,
        pad_x=2.4,
        pad_y=2.2,
        body_x=4.6,
        body_y=2.8,
        pin1_right=True,
    )
    add_smd_2(
        board,
        "D2",
        "SMBJ22A",
        27,
        24,
        nets["GND"],
        nets["VPWR"],
        spacing=6.2,
        pad_x=2.7,
        pad_y=2.4,
        body_x=5.4,
        body_y=3.2,
        pin1_right=True,
    )
    add_smd_2(
        board,
        "C2",
        "100n 50V",
        34,
        24,
        nets["GND"],
        nets["VPWR"],
        spacing=3.2,
    )
    add_smd_2(
        board,
        "C3",
        "47u 50V",
        41,
        24,
        nets["GND"],
        nets["VPWR"],
        spacing=5.0,
        pad_x=2.2,
        pad_y=2.8,
        body_x=4.0,
        body_y=5.5,
    )

    add_smd_2(board, "R3", "10k", 41, 10, nets["OPTO_C"], nets["QBASE"])
    add_smd_2(board, "R4", "100k", 46, 14, nets["QBASE"], nets["VPWR"])
    add_sot23(
        board,
        "Q1",
        "BC807-40",
        51,
        10,
        {1: nets["QBASE"], 2: nets["VPWR"], 3: nets["QCOL"]},
    )
    add_smd_2(board, "R5", "10k", 56, 14, nets["QCOL"], nets["CTRL"])
    add_smd_2(board, "R6", "100k", 62, 18, nets["CTRL"], nets["GND"])
    add_smd_2(
        board,
        "C1",
        "10u 25V",
        62,
        23,
        nets["CTRL"],
        nets["GND"],
        spacing=3.8,
        pad_x=1.8,
        pad_y=2.2,
        body_x=2.8,
        body_y=3.4,
    )
    add_smd_2(
        board,
        "D4",
        "BZT52C5V1",
        56,
        18,
        nets["GND"],
        nets["CTRL"],
        spacing=3.8,
        pad_x=1.7,
        pad_y=1.5,
        pin1_right=True,
    )

    add_soic8(
        board,
        "U1",
        "BSP762TXUMA1",
        69,
        20,
        {
            1: nets["GND"],
            2: nets["CTRL"],
            3: nets["LAMP_OUT"],
            4: None,
            5: nets["VPWR"],
            6: nets["VPWR"],
            7: nets["VPWR"],
            8: nets["VPWR"],
        },
    )

    # Local signal chain on the front layer.
    add_track(board, nets["SENSE"], [(7, 10), (15.4, 10)])
    add_track(board, nets["SENSE_R1"], [(18.6, 10), (21.4, 10)])
    add_track(board, nets["OPTO_A"], [(24.6, 10), (27.5, 10)])
    add_track(board, nets["OPTO_A"], [(24.6, 10), (25.2, 10), (25.2, 14), (24.9, 14)])
    add_track(board, nets["OPTO_C"], [(36.5, 10), (39.4, 10)])
    add_track(board, nets["QBASE"], [(42.6, 10), (45, 10), (45, 12.5), (49.3, 12.5), (49.3, 10.95)])
    add_track(board, nets["QBASE"], [(45, 12.5), (44.4, 14)])
    add_track(board, nets["QCOL"], [(52.7, 10), (54.4, 14)])
    add_track(board, nets["CTRL"], [(57.6, 14), (60.4, 14), (60.4, 18), (60.4, 18)])
    add_track(board, nets["CTRL"], [(60.4, 18), (60.1, 23)])
    add_track(board, nets["CTRL"], [(60.4, 18), (57.9, 18)])
    add_track(board, nets["CTRL"], [(60.4, 18), (59, 18), (59, 19.365), (66, 19.365)])

    # B.Cu buses keep power, output, and ground separated.
    add_track(board, nets["LAMP_OUT"], [(7, 20.16), (12, 20.16), (12, 28), (68, 28)], 1.2, pcbnew.B_Cu)
    add_track(board, nets["VPWR"], [(20, 31), (73, 31)], 1.2, pcbnew.B_Cu)

    # Raw input and series reverse-polarity diode.
    add_track(board, nets["VPRE"], [(7, 15.08), (12, 15.08), (12, 18), (14.25, 18)], 1.2)
    add_track(board, nets["VPWR"], [(19.75, 18), (20, 18), (20, 31)], 1.2)
    add_via(board, nets["VPWR"], 20, 31)

    # VPWR branches from components to the bottom bus.
    add_track(board, nets["VPWR"], [(30.1, 24), (30.1, 31)], 0.8)
    add_via(board, nets["VPWR"], 30.1, 31)
    add_track(board, nets["VPWR"], [(35.6, 24), (35.6, 31)], 0.8)
    add_via(board, nets["VPWR"], 35.6, 31)
    add_track(board, nets["VPWR"], [(43.5, 24), (43.5, 31)], 0.8)
    add_via(board, nets["VPWR"], 43.5, 31)
    add_track(board, nets["VPWR"], [(47.6, 14), (47.6, 16), (51.2, 16), (51.2, 7.5), (49.3, 7.5), (49.3, 9.05)], 0.6)
    add_track(board, nets["VPWR"], [(47.6, 14), (47.6, 31)], 0.6)
    add_via(board, nets["VPWR"], 47.6, 31)
    for py in [18.095, 19.365, 20.635, 21.905]:
        add_track(board, nets["VPWR"], [(72, py), (73, py), (73, 31)], 0.8)
    add_via(board, nets["VPWR"], 73, 31)

    # Ground pads connect through nearby vias to the B.Cu ground pour.
    ground_stubs = [
        ((21.1, 14), (21.1, 15.5)),
        ((27.5, 12.54), (27.5, 14.5)),
        ((36.5, 12.54), (36.5, 14.5)),
        ((23.9, 24), (23.9, 26)),
        ((32.4, 24), (32.4, 26)),
        ((38.5, 24), (38.5, 26.5)),
        ((63.6, 18), (63.6, 16.5)),
        ((63.9, 23), (65.5, 23)),
        ((54.1, 18), (54.1, 20)),
    ]
    for start, end in ground_stubs:
        add_track(board, nets["GND"], [start, end], 0.5)
        add_via(board, nets["GND"], *end)
    add_track(board, nets["GND"], [(66, 18.095), (63.6, 18)], 0.6)

    # Output branch from U1 to its B.Cu bus.
    add_track(board, nets["LAMP_OUT"], [(66, 20.635), (68, 20.635)], 1.2)
    add_via(board, nets["LAMP_OUT"], 68, 20.635)
    add_track(board, nets["LAMP_OUT"], [(68, 20.635), (68, 28)], 1.2, pcbnew.B_Cu)

    add_ground_zone(board, nets["GND"])

    # Labels and polarity notes.
    board_texts = [
        ("F-150 LIGHTNING", 40, 3.5, 1.2),
        ("MARKER LAMP CTRL REV A", 40, 43.0, 1.0),
        ("J1: 1 SENSE  2 BATT+  3 LAMP+  4 GND", 40, 39.5, 0.8),
    ]
    for text, x, y, size in board_texts:
        item = pcbnew.PCB_TEXT(board)
        item.SetText(text)
        item.SetPosition(point(x, y))
        item.SetLayer(pcbnew.F_SilkS)
        item.SetTextSize(point(size, size))
        item.SetTextThickness(MM(0.15))
        board.Add(item)

    pcbnew.SaveBoard(str(BOARD_PATH), board)


if __name__ == "__main__":
    build_board()
    print(BOARD_PATH)
