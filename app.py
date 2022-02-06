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
    [['AK47H', 'Krawi', 'Foreshadow', 'TR33', 'Paintbrush', 'cjay'],
     ['jishua', 'Soko', 'Thunda', 'Doomed', 'Vega', 'moszer']])

DataPoints = {
    'Name': 'Player',
    'Role': 'Role',
    'Hero': 'Hero',
    'Final Blows': 'FBs',
    'Eliminations': 'Elims',
    'Deaths': 'Deaths',
    'Hero Damage Dealt': 'Hero Dmg',
    'Barrier Damage Dealt': 'Barrier Dmg',
    'Healing Dealt': 'Heals Given',
    'Damage Blocked': 'Dmg Blocked',
    'Damage Taken': 'Dmg Taken',
    'Ultimates Earned': 'Ults Earned',
    'Ultimates Used': 'Ults Used'
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
    if WatchingFile != '':
        newLines = []
        with open(WatchingFile, 'r') as f:
            for line in f:
                if line not in readLines:
                    newLines.append(line)
        for line in newLines:
            analyzer.processLine(line)
            readLines.add(line)


@app.route('/')
def index():
    return render_template('index.html', points=DataPoints)


@app.route('/toggle_per_10')
def toggle_per_10():
    return str(analyzer.togglePerTen())


@app.route('/data_table/<int:team_id>')
def data_table(team_id):
    return json.dumps(analyzer.dumpTable(team_id))


@app.route('/data_json')
def data_json():
    checkForUpdates()
    return json.dumps(analyzer.dump())


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
        for i in range(0, 1000):
            analyzer.processLine(testData[i])

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
