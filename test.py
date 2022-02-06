from analyze import Analyzer

# load test file
with open('samples/sample1.txt', 'r') as f:
    testData = [line for line in f]
testAnalyzer = Analyzer(['Team 1', 'Team 2'], [['AK47H', 'Krawi', 'Foreshadow', 'TR33', 'Paintbrush', 'cjay'], ['jishua', 'Soko', 'Thunda', 'Doomed', 'Vega', 'moszer']])

# test processLine
for i in range(0, 1000):
    testAnalyzer.processLine(testData[i])