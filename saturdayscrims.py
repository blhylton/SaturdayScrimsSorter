import csv
from sys import argv
from sys import exit


class TeamList:
    def __init__(self):
        self.teams = []
        self.score_card = {
            'na': 0,
            'eu': 15000,
            'pc': 0,
            'ps': 5000,
            'xb': 10000
        }

    def sort(self):
        for team in self.teams:
            if team.score == 0:
                team.score = team.sr_avg() + \
                    self.score_card[team.region] + \
                    self.score_card[team.platform]
        self.teams.sort()

    def append(self, team):
        self.teams.append(team)


class Team:
    def __init__(self):
        self.team_name = ''
        self.region = ''
        self.platform = ''
        self.captain_discord = ''
        self.players = []
        self._sr_avg = 0
        self.score = 0

    def sr_avg(self):
        if self._sr_avg == 0:
            sum = 0
            for player in self.players:
                sum += player.sr
            self._sr_avg = sum/len(self.players)

        return self._sr_avg

    def __lt__(self, other):
        return self.score < other.score

    def parse_csv_row(self, row):
        self.team_name = row[2]
        self.region = self._handle_region(row[3])
        self.platform = self._handle_platform(row[4])
        self.captain_discord = row[5]

        self.players.append(Player(row[6], row[7], row[8]))
        if row[10] and row[12]:
            self.players.append(Player(row[9], row[10], row[12]))
        if row[14] and row[16]:
            self.players.append(Player(row[13], row[14], row[16]))
        if row[18] and row[20]:
            self.players.append(Player(row[17], row[18], row[20]))
        if row[22] and row[24]:
            self.players.append(Player(row[21], row[22], row[24]))
        if row[26] and row[28]:
            self.players.append(Player(row[25], row[26], row[28]))
        if row[29] == 'Yes':
            self.players.append(Player(row[30], row[31], row[33]))
        if row[34] == 'Yes':
            self.players.append(Player(row[35], row[36], row[38]))

    def _handle_region(self, region_entry):
        if 'Americas' in region_entry:
            return 'na'
        return 'eu'

    def _handle_platform(self, platform_entry):
        if platform_entry == 'PC (Battle.net)':
            return 'pc'
        elif platform_entry == 'Playstation 4':
            return 'ps'
        return 'xb'

    def __str__(self):
        val_str = '{}\tTeam Captain: {}\n```'.format(
            self.team_name, self.captain_discord)
        for player in self.players:
            val_str += str(player)

        return val_str + '```\n'


class Player:
    def __init__(self, discord, battle_tag, sr):
        self.discord = discord
        self.battle_tag = battle_tag
        self.sr = int(sr)

    def __str__(self):
        return '{: <20}{}\n'.format(self.battle_tag, self.discord)


class DuplicateBattleTagException(Exception):
    def __init__(self, message):
        self.message = message


def dedupe(input_file_location):
    with open(input_file_location, 'r', encoding="latin-1", newline='') as input_file:
        battle_tags = {}
        reader = csv.reader(input_file)
        # Ignore header row
        next(reader, None)
        for idx, row in enumerate(reader, start=2):
            if row[5]:
                if row[5] not in battle_tags.values():
                    battle_tags['F' + str(idx)] = row[5]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[5]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'F', str(idx)))
            if row[9]:
                if row[9] not in battle_tags.values():
                    battle_tags['J' + str(idx)] = row[9]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[9]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'J', str(idx)))

            if row[13]:
                if row[13] not in battle_tags.values():
                    battle_tags['N' + str(idx)] = row[13]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[13]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'N', str(idx)))

            if row[17]:
                if row[17] not in battle_tags.values():
                    battle_tags['R' + str(idx)] = row[17]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[17]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'R', str(idx)))

            if row[21]:
                if row[21] not in battle_tags.values():
                    battle_tags['V' + str(idx)] = row[21]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[21]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'V', str(idx)))

            if row[25]:
                if row[25] not in battle_tags.values():
                    battle_tags['Z' + str(idx)] = row[25]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[25]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'Z', str(idx)))

            if row[30]:
                if row[30] not in battle_tags.values():
                    battle_tags['AE' + str(idx)] = row[30]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[30]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'AE', str(idx)))

            if row[35]:
                if row[35] not in battle_tags.values():
                    battle_tags['AJ' + str(idx)] = row[35]
                else:
                    for cell, tag in battle_tags.items():
                        if tag == row[35]:
                            raise DuplicateBattleTagException(
                                'Duplicate battle tag in {} and {}{}'.format(cell, 'AJ', str(idx)))


if 'help' in argv[1]:
    print(
        '\nUsage: scrimsunday <input_file.csv> [pretty_output_file.txt] [importable_output_file.txt]')
    print('\n\tIf no output files are specified, the default files are \'pretty-output.txt\' and \'importable-output.txt\' and will be placed relative to the executable.')
    exit()

input_file = argv[1]
pretty_output_file = argv[2] if len(argv) > 2 else 'pretty-output.txt'
importer_output_file = argv[3] if len(argv) > 3 else 'importable-output.txt'

try:
    dedupe(input_file)
except DuplicateBattleTagException as e:
    print(e.message)
    exit()

Teams = TeamList()

f = open(input_file, 'r', encoding="latin-1", newline='')

reader = csv.reader(f)
# Ignore header row
next(reader, None)
for row in reader:
    if row[0]:
        team = Team()
        team.parse_csv_row(row)
        Teams.append(team)

f.close()

Teams.sort()
with open(pretty_output_file, 'w', encoding='latin-1') as out:
    prevRegion = Teams.teams[0].region + Teams.teams[0].platform
    out.write('\n========== {} - {} =========\n'.format(
        Teams.teams[0].region.upper(), Teams.teams[0].platform.upper()))
    for idx, team in enumerate(Teams.teams, start=1):
        if prevRegion != team.region + team.platform:
            prevRegion = team.region + team.platform
            out.write(
                '\n========== {} - {} =========\n'.format(team.region.upper(), team.platform.upper()))
        out.write(str(team))


with open(importer_output_file, 'w', encoding='latin-1') as out:
    prevRegion = Teams.teams[0].region + Teams.teams[0].platform
    out.write('\n~~~~~~~~~~~~~~~~ {} - {} ~~~~~~~~~~~~~~~~\n'.format(
        Teams.teams[0].region.upper(), Teams.teams[0].platform.upper()))
    for idx, team in enumerate(Teams.teams, start=1):
        if prevRegion != team.region + team.platform:
            prevRegion = team.region + team.platform
            out.write(
                '\n~~~~~~~~~~~~~~~~ {} - {} ~~~~~~~~~~~~~~~~\n'.format(team.region.upper(), team.platform.upper()))
        out.write('{}\t{}\t{}\t{}\n'.format(team.team_name, team.captain_discord,
                                            round(team.sr_avg()), '{} - {}'.format(team.region.upper(), team.platform.upper())))

        for player in team.players:
            out.write('{}\t{}\t{}\n'.format(
                player.battle_tag, player.discord, player.sr))
        out.write('\n')
