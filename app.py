import argparse
import time
import json
from analyze import Analyzer
from config import Config
from flask import Flask, render_template
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)
analyzer = Analyzer(
    ['Team 1', 'Team 2'],
    [['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6'],
     ['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6']])

testData = []
testDataIdx = 0

DataPoints = {
    'Name': 'Player',
    'Role': 'Role',
    'Hero': 'Hero',
    'Impact Score': 'Impact',
    'Final Blows': 'FBs',
    'Eliminations': 'Elims',
    'Deaths': 'Deaths',
    'Hero Damage Dealt': 'Hero Dmg',
    'Barrier Damage Dealt': 'Barrier Dmg',
    'Healing Dealt': 'Heals Given',
    'Damage Blocked': 'Dmg Blocked',
    'Damage Taken': 'Dmg Taken',
    'Ultimates Used / Ultimates Earned': 'Ults Used / Earned'
}

WatchingFile = ''


class LogFileHandler(FileSystemEventHandler):

    def on_created(self, event):
        global WatchingFile
        if '/Log-' in event.src_path:
            if WatchingFile == '':
                WatchingFile = event.src_path
                print('Observing Logfile: ' + WatchingFile)


readLines = set()


def checkForUpdates():
    global testDataIdx
    if WatchingFile != '':
        newLines = []
        with open(WatchingFile, 'r') as f:
            for line in f:
                if line not in readLines:
                    newLines.append(line)
        for line in newLines:
            analyzer.processLine(line)
            readLines.add(line)
    if testDataIdx > 0:
        for i in range(testDataIdx, testDataIdx + 13):
            analyzer.processLine(testData[i])
        testDataIdx += (13)


@app.route('/')
def index():
    return render_template('index.html', points=DataPoints)


@app.route('/toggle_per_10')
def toggle_per_10():
    return str(analyzer.togglePerTen())


@app.route('/data_table/<int:team_id>')
def data_table(team_id):
    return json.dumps(analyzer.dumpTable(team_id))


@app.route('/data_table_delta')
def data_table_delta():
    return json.dumps(analyzer.dumpTableDelta())


@app.route('/data_json')
def data_json():
    checkForUpdates()
    return json.dumps(analyzer.dump())

def autoPageUpdate(number):
    return '<html><head><meta http-equiv="refresh" content="1"></head><body>' + str(number) + '</body></html>'

@app.route('/data_json/team<int:team_id>/player<int:player_id>/<stat_name>')
def data_json_playerstat(team_id, player_id, stat_name):
    return '<html><head><meta http-equiv="refresh" content="1"></head><body>' + str(analyzer.PlayerStats[0][0].Stats[stat_name]) + '</body></html>'


if __name__ == "__main__":

    # grab arguments
    parser = argparse.ArgumentParser("champria_analysis_live")
    parser.add_argument("--port",
                        help="Specify port for web server.",
                        type=int,
                        default=8080)
    parser.add_argument("--test",
                        help="Test mode enabled?",
                        type=bool,
                        default=False)
    parser.add_argument("--debug",
                        help="Run in debug mode.",
                        type=bool,
                        default=False)
    args = parser.parse_args()

    # initialize
    if args.test == False:
        analyzer = Analyzer(Config.Teams, Config.Players)
    else:
        with open('samples/sample1.txt', 'r') as f:
            testData = [line for line in f]
        for i in range(0, 3):
            analyzer.processLine(testData[i])
            testDataIdx = 3

    # start watch agent
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='../Workshop/', recursive=False)
    observer.start()
    try:
        app.run("0.0.0.0", args.port, debug=args.debug)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
