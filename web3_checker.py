import asyncio
import csv
import math

from loguru import logger
from termcolor import cprint
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth

from config import settings, DATA, ERC20_ABI, decimalToInt, outfile, WALLETS

RESULT = {
    'wallets': [],
    'balances': [],
}


def evm_wallet(key):
    retry = 0
    while True:
        try:
            web3 = Web3(Web3.HTTPProvider(DATA['ethereum']['rpc']))
            wallet = web3.eth.account.from_key(key).address
            return wallet
        except:
            retry += 1
            if retry >= 2:
                return key


def round_to(num, digits=3):
    try:
        if num == 0: return 0
        scale = int(-math.floor(math.log10(abs(num - int(num))))) + digits - 1
        if scale < digits: scale = digits
        return round(num, scale)
    except:
        return num


async def check_data_token(web3, token_address):
    try:

        token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
        decimals = await token_contract.functions.decimals().call()
        symbol = await token_contract.functions.symbol().call()

        return token_contract, decimals, symbol

    except Exception as error:

        logger.error(f'{error}')
        await asyncio.sleep(2)
        return await check_data_token(web3, token_address)


async def check_balance(web3, private_key, chain, address_contract):
    try:

        try:
            wallet = web3.eth.account.from_key(private_key)
            wallet = wallet.address
        except Exception as error:
            # logger.error(str(error))
            wallet = private_key

        if address_contract == '':  # eth
            balance = await web3.eth.get_balance(web3.to_checksum_address(wallet))
            token_decimal = 18
        else:
            token_contract, token_decimal, symbol = await check_data_token(web3, address_contract)
            balance = await token_contract.functions.balanceOf(web3.to_checksum_address(wallet)).call()

        human_readable = decimalToInt(balance, token_decimal)

        return human_readable

    except Exception as error:
        logger.error(str(error))
        await asyncio.sleep(1)
        return await check_balance(web3, private_key, chain, address_contract)


async def worker(private_key, chain, address_contract):
    while True:
        try:
            web3 = Web3(AsyncHTTPProvider(DATA[chain]['rpc']),
                        modules={"eth": (AsyncEth,)},
                        middlewares=[],
                        )
            break
        except Exception as error:
            cprint(str(error), 'red')
            await asyncio.sleep(1)

    balance = await check_balance(web3, private_key, chain, address_contract)
    RESULT['wallets'].append({private_key: balance})
    RESULT['balances'].append(balance)


async def main(chain, address_contract, wallets):
    tasks = [worker(wallet, chain, address_contract) for wallet in wallets]
    await asyncio.gather(*tasks)


def send_result(min_balance, file_name, wallets_):
    small_balance = []
    with open(f'{outfile}results/{file_name}.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        spamwriter.writerow(['wallet', 'balance'])

        for address in wallets_:
            for data in RESULT['wallets']:
                for wallets in data.items():
                    wallet = wallets[0]
                    balance = wallets[1]

                    if wallet == address:
                        if balance >= min_balance:
                            balance = round_to(balance)
                            cprint(f'{wallet} : {balance}', 'white')
                            spamwriter.writerow([wallet, balance])
                        else:
                            small_balance.append(wallet)

        sum_balance = sum(RESULT["balances"])
        sum_balance = round_to(sum_balance)
        spamwriter.writerow(['total_balance', sum_balance])

        cprint(f'total balance : {sum_balance}\n', 'green')

        if len(small_balance) != 0:
            cprint(f'\nBalance of these wallets < {min_balance} :', 'yellow')
            spamwriter.writerow([])
            spamwriter.writerow(['small balance:'])
            for wallet in small_balance:
                cprint(wallet, 'white')
                spamwriter.writerow([wallet])

        cprint(f'\nРезультаты записаны в файл : {outfile}results/{file_name}.csv\n', 'blue')


def web3_check(*args):
    cprint(f'\nSTART WEB3 CHECKER\n', 'green')

    RESULT['wallets'].clear()
    RESULT['balances'].clear()

    wallets = []
    for key in WALLETS:
        wallet = evm_wallet(key)
        wallets.append(wallet)

    chain = settings['value_web3_checker']['chain']
    address_contract = settings['value_web3_checker']['address_contract']
    min_balance = settings['value_web3_checker']['min_balance']
    file_name = settings['value_web3_checker']['file_name']

    asyncio.run(main(chain, address_contract, wallets))

    send_result(min_balance, file_name, wallets)
