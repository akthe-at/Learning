import pandas as pd

dfGameboy = pd.read_csv('GameReviews_Gameboy.csv')
dfGameboyAdvance = pd.read_csv('GameReviews_GameboyAdvance.csv')
dfGamecube = pd.read_csv('GameReviews_Gamecube.csv')
dfN64 = pd.read_csv('GameReviews_N64.csv')
dfNes = pd.read_csv('GameReviews_NES.csv')
dfNintendoDS = pd.read_csv('GameReviews_NintendoDS.csv')
dfSNES = pd.read_csv('GameReviews_SNES.csv')
dfSwitch = pd.read_csv('GameReviews_Switch.csv')
dfWii = pd.read_csv('GameReviews_Wii.csv')
dfWiiU = pd.read_csv('GameReviews_WiiU.csv')


df = pd.concat([dfGameboy, dfGameboyAdvance, dfGamecube, dfN64, dfNes, dfNintendoDS, dfSNES, dfSwitch, dfWii, dfWiiU ])
df.to_csv('GameReviews_Nintendo_Overall.csv', index=False)
print(df.sample(n=20))
print('Shape')
print(df.shape)