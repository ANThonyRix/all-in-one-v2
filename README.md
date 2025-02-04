[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=All-in-one+V2)](https://git.io/typing-svg)

Идеальный скрипт-V2 для ведения фермы. Освоив его, ты сможешь (идет перечисление модулей) :

1. web3_checker : очень быстро (асинка) смотрит баланс монеты в любой evm сети.
2. debank_checker : около_быстро (асинка) смотрит все токены, нфт и протоколы во всех evm сетях (которые доступны на самом [debank](https://debank.com/)). 
3. exchange_withdraw : вывод монет с бирж : binance, mexc, kucoin, bybit, huobi.
4. okx_withdraw : вывод с биржи okx + в подарок вывод с субов. отдельным модулем из-за функции вывода с суб-аккаунтов.
5. transfer : вывод монет с кошельков в evm сетях (метамаск).
6. 1inch : свапы на 1inch во всех сетях, включая zksync era.
7. [orbiter](https://www.orbiter.finance/) : бридж eth во всех сетях, включая zksync era и starknet. чтобы бриджит на starknet, нужно добавить адреса кошельков старкнета в файл `starknet_address.txt`.
8. [woofi](https://fi.woo.org/) : бриджи и свапы. бридж проходит через stargate (layerzero). универсален, доступны все монеты и сети, которые там есть. 

Дополнительная информация :
1. Вместо принтов сделал logger. 
2. Добавил tg_sender. Все результаты прописываются не только в терминал, но и в тг-бота.
3. Для чекеров сделал csv файлы. 
4. Сделал нормальные try exceptы.
5. Сделал проверку транзакций на фейл (check_status_tx).
6. Сделал универсальный апрув и предварительную проверку на кол-во апрувнутых монет (check_allowance). то есть лишних апрувов делать не будет.

# Настройка.

1. Вся настройка модулей и апи ключей делается в файле `setting.yaml`, их настройка описана в этом же файле. 
2.  В папке data есть 3 файла : `wallets.txt`, `recipients.txt`, `proxies.txt` :
- `wallets.txt` - сюда записываем кошельки (приватники / адреса).
- `recipients.txt` - сюда записываем адреса для трансфера, используется только в модуле transfer когда выводим с кошелька на адрес. 1 кошелек = 1 адрес.
- `proxies.txt` - сюда записываем прокси, они используются только в debank чекере, без них он работать не будет. Чем больше, тем лучше. Формат : http://login:password@ip:port
- `starknet_address.txt` - сюда записываем адреса кошельков старкнета. если не будете бриджить с орбитера на старкнет, можно не вставлять.
- `rpc.py` - здесь по желанию (необязательно, сейчас стоят паблик ankr rpc) нужно менять rpc.
3. Настраивать модули нужно в файле `setting.yaml`.
4. Не забудь настроить тг-бота. Для этого в файле `setting.yaml` в переменную `tg_token` нужно вставить токен от тг бота. В переменную `tg_id` нужно вставить свой id токен, узнать его можно здесь : https://t.me/getmyid_bot.
5. Запускать нужно файл `MAIN.py`

Устанавливаем библиотеки : `pip3 install -r requirements.txt`

Огромная просьба сначала все прочитать на 10 раз, все протестировать, погуглить и только потом задавать вопросы в наш код чат. В личку админам с вопросами по коду просьба не писать, они не ответят.

Donate (evm) : `0xb7415DB78c886c67DBfB25D3Eb7fcd496dAf9021` or `donates-for-hodlmod.eth`

Паблик : https://t.me/hodlmodeth. [ code ] чат : https://t.me/code_hodlmodeth.
