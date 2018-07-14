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
"""A module for python-chess which outputs an HTML table of a board.

This file is currently in a beta, proof-of-concept stage.
"""

import chess

TABLE_HEAD = """<table class="chess_board">"""
TABLE_HEAD_COORDS = """<thead>
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
<tfoot>
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
<colgroup>
    <col span="1" class="rank-names">
    <col span="8" class"board">
    <col span="1" class"rank-names">
 </colgroup>
"""
TABLE_ROW_HEAD = """<tr>"""
TABLE_ROW_COORDS = """<th>{rank}</th>"""
TABLE_ATTACK = """<a href="#" class="attack">&times;</a>"""
TABLE_DATA = """<td id="{square}" class="{lastmove}">{attack}<a href="#" class="{piece_name} {color} {check}">{symbol}</a></td>
"""
TABLE_ROW_FOOT = """</tr>"""
TABLE_FOOT = """</table>"""

def piece(piece: chess.Piece):
    """Renders the given :class:`chess.Piece` as HTML escaped unicode.
    """
    return piece.unicode_symbol().encode('ascii', 'xmlcharrefreplace').decode()


def board(board: chess.Board, squares=[], flipped=False, coordinates=True,
          lastmove=None, check=None):
    """
    Renders a board with pieces and/or selected squares as an HTML table.

    :param board: A :class:`chess.BaseBoard` for a chessboard with pieces or
        ``None`` (the default) for a chessboard without pieces.
    :param squares: A :class:`chess.SquareSet` with selected squares.
    :param flipped: Pass ``True`` to flip the board.
    :param coordinates: Pass ``False`` to disable coordinates in the margin.
    :param lastmove: A :class:`chess.Move` to be highlighted.
    :param check: A square to be marked as check.
    """
    html = TABLE_HEAD
    if coordinates:
        html += TABLE_HEAD_COORDS
    if flipped:
        rank_names = chess.RANK_NAMES
    else:
        rank_names = chess.RANK_NAMES[::-1]
    for rank in rank_names:
        html += TABLE_ROW_HEAD
        if coordinates:
            html += TABLE_ROW_COORDS.format(rank=rank)
        for file in chess.FILE_NAMES:
            square = chess.square(chess.FILE_NAMES.index(file),
                                  chess.RANK_NAMES.index(rank))
            data = {'square': chess.square_name(square), 'piece_name': '',
                    'color': '', 'symbol': '', 'attack': '', 'check': '',
                    'lastmove': ''}
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
            html += TABLE_DATA.format(**data)
        if coordinates:
            html += TABLE_ROW_COORDS.format(rank=rank)
        html += TABLE_ROW_FOOT
    html += TABLE_FOOT
    return html
