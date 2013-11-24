from xAPIConnector import *
from settings import USERID, PASSWORD

# settings

SERVER          = 'xapia.x-station.eu'
PORT            = 5124
STREAMING_PORT  = 5125

# the program will end after this time
TIMEOUT = 5

# number of symbols to print
SYMBOLS_TO_PRINT = 5

def main():
    # create new api client and connect to the SERVER
    apiClient = APIClient(address=SERVER, port=PORT, encrypt=True)

    # prepare the login command
    loginCmd = loginCommand(USERID, PASSWORD)

    # execute login command and get streaming session ID
    loginResponse = apiClient.execute(loginCmd)
    streamSessionId = loginResponse['streamSessionId']

    print('Logged in as ' + str(USERID))

    # create new stream client with given stream session ID
    streamClient = APIStreamClient(address=SERVER, port=STREAMING_PORT, ssId=streamSessionId, tickFun=processStreamingTick)

    print('Streaming opened')

    # prepare get server time command
    getServerTimeCmd = baseCommand('getServerTime', dict())

    # get server time
    getServerTimeResponse = apiClient.execute(getServerTimeCmd)

    print('Server time: ' + str(getServerTimeResponse['returnData']['timeString']))

    # prepare get all symbols command
    getAllSymbolsCmd = baseCommand('getAllSymbols', dict())

    # get list of all symbols
    allSymbolsResponse = apiClient.execute(getAllSymbolsCmd)

    print('First ' + str(SYMBOLS_TO_PRINT) + ' symbols:')

    # print first five symbols
    i = 0
    for symbol in allSymbolsResponse['returnData']:
        if i >= SYMBOLS_TO_PRINT:
            break
        print(symbol['symbol'])
        i+=1

    # subscribe for prices
    streamClient.subscribePrices(['EURUSD', 'EURGBP'])

    # this is an example, make it run for 5 seconds
    time.sleep(TIMEOUT)

    # close streaming socket
    streamClient.disconnect()

    # close api socket
    apiClient.disconnect()

def processStreamingTick(msg): 
    print('Tick arrived! ' + str(msg['data']['symbol']) + " ask: " + str(msg['data']['ask']) + " bid: " + str(msg['data']['bid']))

if __name__ == "__main__":
    main()
