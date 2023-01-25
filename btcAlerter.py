import yfinance as yf
import requests
from playsound import playsound
import time

BLOCK_REWARD = 6.25
MINUTES_PER_DAY = 24 * 60


def get_btc_price():
    btc_usd = yf.Ticker('BTC-USD')
    btc_data = btc_usd.history(period='1d', interval='1m')
    return btc_data['Close'][-1]


def get_network_hashrate():
    btc_data = requests.get('https://api.blockchain.info/stats')
    return btc_data.json()['hash_rate']


def get_block_time():
    btc_data = requests.get('https://api.blockchain.info/stats')
    return btc_data.json()['minutes_between_blocks']


def mining_cost(machine_wattage, electricity_cost):
    """
    params: machine_wattage:
                The wattage of your machine/hardware in Wh

            electricity_cost:
                The electricity cost in your country/area in $/kWh

    return:   returns the cost incured from mining bitcoin(for a day) in $/kWh
    """

    machine_usage_per_day = (machine_wattage/1000) * 24
    cost_per_day = machine_usage_per_day * electricity_cost
    return cost_per_day


def mining_revenue(network_hashrate, machine_hashrate, block_time, btc_price):
    """
    params: network_hashrate: 
                The hashrate of the total network in TH/s(Terahashes per second)

            machine_hashrate:
                The hashrate of your own machine in TH/s

            block_reward:
                The amount paid(in btc) for mining one block of btc

            block_time:
                The avg time taken to mine one block of btc(around 10 minutes rn)

    return:   returns the revenue earned my mining bitcoins
    """

    machine_hashrate_share = machine_hashrate/network_hashrate
    blocks_mined_per_day = MINUTES_PER_DAY/block_time
    total_network_revenue = blocks_mined_per_day * BLOCK_REWARD

    machine_revenue = machine_hashrate_share * total_network_revenue * btc_price

    return machine_revenue


def is_mining_profitable(btc_price, network_hashrate, block_time, machine_hashrate=4.3, machine_wattage=45,
                         electricity_cost=0.0812):
    """
    params: btc_price:
                The current bitcoin price in the specified currency (USD by default)

            network_hashrate: 
                The hashrate of the total network in TH/s (Terahashes per second)

            block_time:
                The avg time taken to mine one block of btc(around 10 minutes rn)

            machine_hashrate:
                The hashrate of your own machine in TH/s (Terahashes per second)

            block_reward:
                The amount paid(in btc) for mining one block of btc

            machine_wattage:
                The wattage of your machine/hardware in Wh

            electricity_cost:
                The electricity cost in your country/area in USD/kWh


    return:   returns the revenue earned my mining bitcoins
    """

    cost = mining_cost(machine_wattage, electricity_cost)
    revenue = mining_revenue(
        network_hashrate, machine_hashrate, block_time, btc_price)
    profit = revenue - cost

    if (profit > 0):
        return True
    else:
        return False


def print_btc_info(btc_price, network_hashrate, block_time):
    """
    params: btc_price:
                The current bitcoin price in the specified currency (USD by default)

            network_hashrate: 
                The hashrate of the total network in TH/s (Terahashes per second)

            block_time:
                The avg time taken to mine one block of btc(around 10 minutes currently)

    return:   prints the supplied bitcoin info
    """

    print("The price of Bitcoin is ", btc_price)
    print("The Bitcoin network's hashrate is", network_hashrate)
    print("The time interval between two successive blocks is ", block_time)
    print("\n")


def print_profitability_status(is_profitable):
    """
    param: is_profitable:
                boolean value specifying if bitcoin is profitable to mine or not

    return:   prints the profitability status of bitcoin mining
    """

    if (is_profitable):
        print("Bitcoin is profitable to mine")
    else:
        print("Bitcoin is NOT profitable to mine")


def main():
    # Get user's machine specs and the electricity cost
    machine_wattage = float(
        input("What is your machine's power consumption(in Watt hour)?: "))
    machine_hashrate = float(
        input("What is your machine's hashrate(in TH/s)?: "))
    electricity_cost = float(
        input("What is the electricity cost in your region(in USD/kWh): "))

    was_profitable = None
    while (True):
        btc_price = get_btc_price()
        network_hashrate = (get_network_hashrate()//1000)
        block_time = get_block_time()
        is_profitable = is_mining_profitable(
            btc_price, network_hashrate, block_time, machine_wattage, machine_hashrate, electricity_cost)

        print_btc_info(btc_price, network_hashrate, block_time)

        """
        if(is_profitable == True):
            playsound('alert (online-audio-converter.com).mp3')

        """

        if (was_profitable == False):
            print_profitability_status(is_profitable)
            was_profitable = is_profitable

        if (was_profitable != None and is_profitable != was_profitable):
            was_profitable = is_profitable
            playsound('sounds/alert (online-audio-converter.com).mp3')
            print_profitability_status(is_profitable)

        time.sleep(60)


if __name__ == '__main__':
    main()
