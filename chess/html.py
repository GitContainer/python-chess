# -*- coding: utf-8 -*-
# This file is an addition to the python-chess library.
# Copyright (C) 2018 John Jackson <jbpjackson@icloud.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
"""A module for python-chess which outputs an HTML table of a board."""

import chess

HTML_HEAD = """<!doctype html>
<html>
    <head>
        <title>python-chess output</title>
        <style>{style}</style>
    </head>
<body>
"""
DEFAULT_CSS = """.chess_board {
    font-size:4em;
    font-family: sans-serif;
    border-collapse: collapse;
    border-spacing: 0;
    margin-left: auto;
    margin-right: auto;
}
.chess_board .piece {
    color:#000;
    display:block;
    height:1.25em;
    width:1.25em;
    position:relative;
    text-decoration:none;
}
.chess_board td {
    background: rgba(209, 139, 71, 1);
    height:1.25em;
    width:1.25em;
    padding: 0;
    text-align:center;
    vertical-align:middle;
}
.chess_board td.lastmove {
    background: #aaa23b;
}
.chess_board tr:nth-child(odd) td:nth-child(even),
.chess_board tr:nth-child(even) td:nth-child(odd) {
    background:rgba(255, 206, 158, 1);
}
.chess_board tr:nth-child(odd) td:nth-child(even).lastmove,
.chess_board tr:nth-child(even) td:nth-child(odd).lastmove {
    background: #cdd16a;
}
.chess_board th {
    background: transparent;
    height:2.5em;
    width:2.5em;
    padding: 0;
    text-align:center;
    vertical-align:middle;
    font-weight: normal;
    font-size:.5em;
    text-transform: uppercase;
}
.chess_board .check {
    background: -moz-radial-gradient(center, ellipse cover, rgba(255,0,0,1) 0%, rgba(231,0,0,0.5) 50%, rgba(158,0,0,0) 100%);
    background: -webkit-radial-gradient(center, ellipse cover, rgba(255,0,0,1) 0%,rgba(231,0,0,0.5) 50%,rgba(158,0,0,0) 100%);
    background: radial-gradient(ellipse at center, rgba(255,0,0,1) 0%,rgba(231,0,0,0.5) 50%,rgba(158,0,0,0) 100%);
    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#ff0000', endColorstr='#009e0000',GradientType=1 );
}
.chess_board .attack {
    position: absolute;
    z-index: 999;
    display: block;
    width: 1.25em;
    height: 1.25em;
}
"""
TABLE_START = """<table class="chess_board">
"""
TABLE_HEAD_COORDS = """<colgroup>
<col span="1" class="rank-names">
<col span="8" class="board">
<col span="1" class="rank-names">
</colgroup>
<thead>
<tr>
<th></th>
<th>a</th>
<th>b</th>
<th>c</th>
<th>d</th>
<th>e</th>
<th>f</th>
<th>g</th>
<th>h</th>
<th></th>
</tr>
</thead>
"""
TABLE_BODY_START = """<tbody>
"""
TABLE_ROW_START = """<tr>
"""
TABLE_ROW_COORDS = """<th>{rank}</th>
"""
TABLE_DATA = """<td id="{square}" class="{lastmove}">{attack}{piece}</td>
"""
TABLE_ATTACK = """<span class="attack">&times;</a>"""
TABLE_PIECE = """<span class="piece {piece_name} {color} {check}">{symbol}</span>"""
TABLE_ROW_END = """</tr>
"""
TABLE_BODY_END = """</tbody>
"""
TABLE_FOOT_COORDS = """<tfoot>
<tr>
<th></th>
<th>a</th>
<th>b</th>
<th>c</th>
<th>d</th>
<th>e</th>
<th>f</th>
<th>g</th>
<th>h</th>
<th></th>
</tr>
</tfoot>
"""
TABLE_END = """</table>
"""

def piece(piece: chess.Piece):
    """Renders the given :class:`chess.Piece` as HTML escaped unicode.
    """
    return piece.unicode_symbol().encode('ascii', 'xmlcharrefreplace').decode()


def board(board: chess.Board, squares=[], flipped=False, coordinates=True,
          lastmove=None, check=None, snippet=True, style=None):
    """Renders a board with pieces and/or selected squares as an HTML table.

    :param board: A :class:`chess.BaseBoard` for a chessboard with pieces or
        ``None`` (the default) for a chessboard without pieces.
    :param squares: A :class:`chess.SquareSet` with selected squares.
    :param flipped: Pass ``True`` to flip the board.
    :param coordinates: Pass ``False`` to disable coordinates in the margin.
    :param lastmove: A :class:`chess.Move` to be highlighted.
    :param check: A square to be marked as check.
    :param snippet: Pass ``False`` to return a complete HTML document.
    :param style: A CSS stylesheet to include in the HTML document. Has no effect if ``snippet`` is ``True``.
    """
    if snippet:
        html = TABLE_START
    else:
        if not style:
            style = DEFAULT_CSS
        html = HTML_HEAD.format(style=style)
        html += TABLE_START
    if coordinates:
        html += TABLE_HEAD_COORDS
    if flipped:
        rank_names = chess.RANK_NAMES
    else:
        rank_names = chess.RANK_NAMES[::-1]
    html += TABLE_BODY_START
    for rank in rank_names:
        html += TABLE_ROW_START
        if coordinates:
            html += TABLE_ROW_COORDS.format(rank=rank)
        for file in chess.FILE_NAMES:
            square = chess.square(chess.FILE_NAMES.index(file),
                                  chess.RANK_NAMES.index(rank))
            data = {'square': chess.square_name(square), 'piece_name': '',
                    'color': '', 'symbol': '', 'attack': '', 'check': '',
                    'lastmove': '', 'piece': ''}
            if square in squares:
                data['attack'] = TABLE_ATTACK
            if lastmove and square in [lastmove.from_square,
                                       lastmove.to_square]:
                data['lastmove'] = 'lastmove'
            if square in board.piece_map():
                piece_obj = board.piece_map()[square]
                data['symbol'] = piece(piece_obj)
                data['color'] = chess.COLOR_NAMES[piece_obj.color]
                data['piece_name'] = chess.PIECE_NAMES[piece_obj.piece_type]
                if square == check:
                    data['check'] = 'check'
                elif (board.is_check() and piece_obj.piece_type == chess.KING
                      and board.turn == piece_obj.color):
                    data['check'] = 'check'
                data['piece'] = TABLE_PIECE.format(**data)
            html += TABLE_DATA.format(**data)
        if coordinates:
            html += TABLE_ROW_COORDS.format(rank=rank)
        html += TABLE_ROW_END
    html += TABLE_BODY_END
    if coordinates:
        html += TABLE_FOOT_COORDS
    html += TABLE_END
    return html
