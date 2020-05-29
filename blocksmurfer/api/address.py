from flask import jsonify, abort
from flask_restful import marshal, request
from blocksmurfer.api import bp
# from blocksmurfer.api.errors import resp_error
from blocksmurfer.api.structures import transaction_fields, utxo_fields
from blocksmurfer.explorer.service import *


@bp.route('/<string:network>/transactions/<string:address>')
def transactions(network, address):
    after_txid = request.args.get('after_txid', '', type=str)
    if after_txid and not check_txid(after_txid):
        abort(422, "Invalid after_txid provided")
    limit = request.args.get('limit', 10, type=int)
    if limit > 10:
        limit = 10
    srv = SmurferService(network)
    if not check_address(address):
        abort(422, message="Invalid address")
    txs = srv.gettransactions(address, after_txid=after_txid, limit=limit)
    txs_dict = marshal(txs, transaction_fields)
    return jsonify(txs_dict)


@bp.route('/<string:network>/utxos/<string:address>')
def utxos(network, address):
    after_txid = request.args.get('after_txid', '', type=str)
    if after_txid and not check_txid(after_txid):
        abort(422, "Invalid after_txid provided")
    limit = request.args.get('limit', 10, type=int)
    if limit > 10:
        limit = 10
    srv = SmurferService(network)
    if not check_address(address):
        abort(422, message="Invalid address")

    txs = srv.getutxos(address, after_txid=after_txid, limit=limit)
    txs_dict = marshal(txs, utxo_fields)
    return jsonify(txs_dict)


@bp.route('/<string:network>/address_balance/<string:address>')
def address_balance(network, address):
    srv = SmurferService(network)
    if not check_address(address):
        abort(422, message="Invalid address")
    balance = srv.getbalance(address)
    data = {
        'address': address,
        'balance': balance
    }
    return jsonify(data)
