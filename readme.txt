przykładowa implementacja serwera json-rpc, której jedyną funkcją obecnie jest pobieranie pogody z accuwheather dla podanego miasta.

komponenty:
rpc_client.py
	uruchamiamy "python rpc_client.pl --city wrocław"
	jego zadaniem jest ustanowienie połączenia ze zdalnym serwerem rpc znajdującym się pod adresem i porcie podanym w parametrze
	wywołuje funkcję "pogoda.dajdla(--city)" na zdalnym serwerze i wyświetla otrzymaną odpowiedź.

	parametry:
	parser.add_argument('--host', default='127.0.0.1', help='host address')
	parser.add_argument('--port', type=int, default=6666, help='host port number')
	parser.add_argument('--city', default='wrocław', help='city name')

rpcs.py
	serwer rpc uruchamiamy "python rpc_server.py --vv"
	udostepnia api na danym adresie i porcie obsługujące selenium.
	przeglądarka kontrolowana przez selenium może być ukryta (standardowo --hide_browser=True), lub można wymusić jej pokazanie (=False)
	serwer loguje wszelkie wywołania i dane
	serwer może być zdalny, jak i działać lokalnie (bez różnicy, ta sama idea)
	główna funkcja: udostępnianie publicznych funkcji (u nas "dajdla" w klasie "pogoda"), tak aby każdy klient mógł ją wywołać.
	serwer rpc (tinyrpc) działa w oparciu o bibliotekę zmq (zeromq, 0mq) która obsługuje funkcje transportowe.

	parametry:
	parser.add_argument('--host', default='127.0.0.1', help='host address')
	parser.add_argument('--port', type=int, default=6666, help='host port number')
	parser.add_argument('--logfile', default=None, help='logfile name, default=stderr')
	parser.add_argument('--browser', help='browser name', default='firefox')
	parser.add_argument('--hide_browser', default=True, help='use xvfb to run browser')
	parser.add_argument('-v', '--verbose', action='count', help='be more verbose')
