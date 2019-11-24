import math
import random
from operator import attrgetter
import numpy as np

from . import message_parser
from . import sp_exceptions
from . import game_object

static_list=[
     (0.00, 0.025019, 0.025019),
     (0.10, 0.100178, 0.050142),
     (0.20, 0.200321, 0.050003),
     (0.30, 0.301007, 0.050684),
     (0.40, 0.401636, 0.049945),
     (0.50, 0.501572, 0.049991),
     (0.60, 0.599413, 0.047852),
     (0.70, 0.699639, 0.052376),
     (0.80, 0.799954, 0.047940),
     (0.90, 0.897190, 0.049297),
     (1.00, 0.996257, 0.049771),
     (1.10, 1.095282, 0.049255),
     (1.20, 1.198429, 0.053893),
     (1.30, 1.304474, 0.052152),
     (1.40, 1.405808, 0.049183),
     (1.50, 1.499977, 0.044986),
     (1.60, 1.600974, 0.056011),
     (1.70, 1.699463, 0.042478),
     (1.80, 1.795798, 0.053858),
     (1.90, 1.897073, 0.047417),
     (2.00, 1.994338, 0.049849),
     (2.10, 2.096590, 0.052405),
     (2.20, 2.204085, 0.055091),
     (2.30, 2.305275, 0.046100),
     (2.40, 2.399355, 0.047981),
     (2.50, 2.497274, 0.049940),
     (2.60, 2.599191, 0.051978),
     (2.70, 2.705266, 0.054099),
     (2.80, 2.801381, 0.042018),
     (2.90, 2.901419, 0.058021),
     (3.00, 3.004504, 0.045065),
     (3.10, 3.096005, 0.046437),
     (3.20, 3.190292, 0.047851),
     (3.30, 3.287451, 0.049309),
     (3.40, 3.387569, 0.050810),
     (3.50, 3.490736, 0.052358),
     (3.60, 3.597044, 0.053952),
     (3.70, 3.706591, 0.055596),
     (3.80, 3.800186, 0.038001),
     (3.90, 3.896632, 0.058446),
     (4.00, 3.995026, 0.039950),
     (4.10, 4.096416, 0.061442),
     (4.20, 4.199855, 0.041998),
     (4.30, 4.306444, 0.064592),
     (4.40, 4.415186, 0.044151),
     (4.50, 4.504379, 0.045043),
     (4.60, 4.595374, 0.045953),
     (4.70, 4.688206, 0.046881),
     (4.80, 4.782914, 0.047828),
     (4.90, 4.879536, 0.048795),
     (5.00, 4.978109, 0.049780),
     (5.10, 5.078673, 0.050786),
     (5.20, 5.181269, 0.051812),
     (5.30, 5.285938, 0.052859),
     (5.40, 5.392721, 0.053926),
     (5.50, 5.501661, 0.055016),
     (5.60, 5.612802, 0.056127),
     (5.70, 5.697415, 0.028488),
     (5.80, 5.783737, 0.057836),
     (5.90, 5.900576, 0.059004),
     (6.00, 6.019776, 0.060197),
     (6.10, 6.110524, 0.030553),
     (6.20, 6.203106, 0.062030),
     (6.30, 6.296617, 0.031483),
     (6.40, 6.392018, 0.063919),
     (6.50, 6.488378, 0.032443),
     (6.60, 6.586684, 0.065865),
     (6.70, 6.685978, 0.033430),
     (6.80, 6.787278, 0.067871),
     (6.90, 6.889597, 0.034449),
     (7.00, 6.993982, 0.069938),
     (7.10, 7.099416, 0.035497),
     (7.20, 7.206980, 0.072068),
     (7.30, 7.315626, 0.036579),
     (7.40, 7.389149, 0.036946),
     (7.50, 7.501102, 0.075009),
     (7.60, 7.614182, 0.038072),
     (7.70, 7.690706, 0.038454),
     (7.80, 7.807228, 0.078070),
     (7.90, 7.924922, 0.039625),
     (8.00, 8.004569, 0.040023),
     (8.10, 8.085016, 0.040425),
     (8.20, 8.207513, 0.082073),
     (8.30, 8.331242, 0.041656),
     (8.40, 8.414972, 0.042075),
     (8.50, 8.499544, 0.042498),
     (8.60, 8.584966, 0.042925),
     (8.70, 8.671246, 0.043356),
     (8.80, 8.802625, 0.088024),
     (8.90, 8.935325, 0.044677),
     (9.00, 9.025126, 0.045125),
     (9.10, 9.115830, 0.045579),
     (9.20, 9.207446, 0.046037),
     (9.30, 9.299982, 0.046500),
     (9.40, 9.393448, 0.046967),
     (9.50, 9.487854, 0.047439),
     (9.60, 9.583209, 0.047916),
     (9.70, 9.679522, 0.048398),
     (9.80, 9.776803, 0.048884),
     (9.90, 9.875061, 0.049375),
     (10.00, 9.974307, 0.049871),
     (10.10, 10.074550, 0.050372),
     (10.20, 10.175801, 0.050879),
     (10.30, 10.278070, 0.051390),
     (10.40, 10.381366, 0.051907),
     (10.50, 10.485700, 0.052428),
     (10.60, 10.591083, 0.052955),
     (10.70, 10.697526, 0.053488),
     (10.80, 10.805038, 0.054025),
     (10.90, 10.913630, 0.054568),
     (11.00, 11.023314, 0.055116),
     (11.10, 11.134100, 0.055670),
     (11.20, 11.246000, 0.056230),
     (11.40, 11.359024, 0.056795),
     (11.50, 11.473184, 0.057366),
     (11.60, 11.588491, 0.057942),
     (11.70, 11.704958, 0.058525),
     (11.80, 11.822595, 0.059113),
     (11.90, 11.941414, 0.059707),
     (12.10, 12.061427, 0.060307),
     (12.20, 12.182646, 0.060913),
     (12.30, 12.305083, 0.061525),
     (12.40, 12.428752, 0.062144),
     (12.60, 12.553663, 0.062768),
     (12.70, 12.679829, 0.063399),
     (12.80, 12.807264, 0.064036),
     (12.90, 12.935979, 0.064680),
     (13.10, 13.065988, 0.065330),
     (13.20, 13.197303, 0.065986),
     (13.30, 13.329938, 0.066649),
     (13.50, 13.463906, 0.067319),
     (13.60, 13.599221, 0.067996),
     (13.70, 13.735895, 0.068679),
     (13.90, 13.873943, 0.069369),
     (14.00, 14.013379, 0.070067),
     (14.20, 14.154216, 0.070771),
     (14.30, 14.296468, 0.071482),
     (14.40, 14.440149, 0.072200),
     (14.60, 14.585275, 0.072926),
     (14.70, 14.731860, 0.073659),
     (14.90, 14.879917, 0.074399),
     (15.00, 15.029463, 0.075147),
     (15.20, 15.180512, 0.075902),
     (15.30, 15.333078, 0.076665),
     (15.50, 15.487178, 0.077435),
     (15.60, 15.642827, 0.078214),
     (15.80, 15.800040, 0.079000),
     (16.00, 15.958833, 0.079794),
     (16.10, 16.119222, 0.080596),
     (16.30, 16.281223, 0.081406),
     (16.40, 16.444852, 0.082224),
     (16.60, 16.610125, 0.083051),
     (16.80, 16.777060, 0.083885),
     (16.90, 16.945672, 0.084729),
     (17.10, 17.115979, 0.085580),
     (17.30, 17.287998, 0.086440),
     (17.50, 17.461745, 0.087309),
     (17.60, 17.637239, 0.088186),
     (17.80, 17.814496, 0.089072),
     (18.00, 17.993534, 0.089968),
     (18.20, 18.174372, 0.090872),
     (18.40, 18.357028, 0.091785),
     (18.50, 18.541519, 0.092708),
     (18.70, 18.727865, 0.093639),
     (18.90, 18.916083, 0.094580),
     (19.10, 19.106192, 0.095531),
     (19.30, 19.298213, 0.096491),
     (19.50, 19.492163, 0.097461),
     (19.70, 19.688063, 0.098440),
     (19.90, 19.885931, 0.099429),
     (20.10, 20.085788, 0.100429),
     (20.30, 20.287653, 0.101438),
     (20.50, 20.491547, 0.102458),
     (20.70, 20.697491, 0.103487),
     (20.90, 20.905504, 0.104528),
     (21.10, 21.115609, 0.105578),
     (21.30, 21.327824, 0.106639),
     (21.50, 21.542172, 0.107711),
     (21.80, 21.758674, 0.108793),
     (22.00, 21.977353, 0.109887),
     (22.20, 22.198229, 0.110991),
     (22.40, 22.421325, 0.112107),
     (22.60, 22.646663, 0.113233),
     (22.90, 22.874266, 0.114371),
     (23.10, 23.104156, 0.115521),
     (23.30, 23.336357, 0.116682),
     (23.60, 23.570891, 0.117854),
     (23.80, 23.807782, 0.119038),
     (24.00, 24.047054, 0.120235),
     (24.30, 24.288731, 0.121443),
     (24.50, 24.532837, 0.122664),
     (24.80, 24.779396, 0.123896),
     (25.00, 25.028433, 0.125142),
     (25.30, 25.279973, 0.126399),
     (25.50, 25.534041, 0.127670),
     (25.80, 25.790663, 0.128953),
     (26.00, 26.049863, 0.130249),
     (26.30, 26.311668, 0.131558),
     (26.60, 26.576105, 0.132880),
     (26.80, 26.843200, 0.134216),
     (27.10, 27.112978, 0.135564),
     (27.40, 27.385468, 0.136927),
     (27.70, 27.660696, 0.138303),
     (27.90, 27.938691, 0.139693),
     (28.20, 28.219480, 0.141097),
     (28.50, 28.503090, 0.142515),
     (28.80, 28.789551, 0.143947),
     (29.10, 29.078891, 0.145394),
     (29.40, 29.371138, 0.146855),
     (29.70, 29.666323, 0.148331),
     (30.00, 29.964475, 0.149822),
     (30.30, 30.265623, 0.151328),
     (30.60, 30.569797, 0.152848),
     (30.90, 30.877029, 0.154385),
     (31.20, 31.187348, 0.155936),
     (31.50, 31.500786, 0.157503),
     (31.80, 31.817374, 0.159086),
     (32.10, 32.137144, 0.160685),
     (32.50, 32.460128, 0.162300),
     (32.80, 32.786358, 0.163930),
     (33.10, 33.115866, 0.165578),
     (33.40, 33.448686, 0.167242),
     (33.80, 33.784851, 0.168923),
     (34.10, 34.124394, 0.170621),
     (34.50, 34.467350, 0.172336),
     (34.80, 34.813753, 0.174067),
     (35.20, 35.163637, 0.175817),
     (35.50, 35.517037, 0.177584),
     (35.90, 35.873989, 0.179369),
     (36.20, 36.234529, 0.181171),
     (36.60, 36.598691, 0.182992),
     (37.00, 36.966514, 0.184831),
     (37.30, 37.338034, 0.186689),
     (37.70, 37.713288, 0.188565),
     (38.10, 38.092312, 0.190460),
     (38.50, 38.475147, 0.192375),
     (38.90, 38.861829, 0.194308),
     (39.30, 39.252396, 0.196260),
     (39.60, 39.646889, 0.198233),
     (40.00, 40.045347, 0.200225),
     (40.40, 40.447810, 0.202238),
     (40.90, 40.854317, 0.204270),
     (41.30, 41.264910, 0.206323),
     (41.70, 41.679629, 0.208397),
     (42.10, 42.098516, 0.210491),
     (42.50, 42.521613, 0.212606),
     (42.90, 42.948962, 0.214743),
     (43.40, 43.380607, 0.216902),
     (43.80, 43.816589, 0.219081),
     (44.30, 44.256953, 0.221283),
     (44.70, 44.701743, 0.223507),
     (45.20, 45.151003, 0.225753),
     (45.60, 45.604778, 0.228022),
     (46.10, 46.063114, 0.230314),
     (46.50, 46.526056, 0.232629),
     (47.00, 46.993650, 0.234966),
     (47.50, 47.465944, 0.237328),
     (47.90, 47.942985, 0.239713),
     (48.40, 48.424820, 0.242122),
     (48.90, 48.911498, 0.244556),
     (49.40, 49.403066, 0.247013),
     (49.90, 49.899575, 0.249496),
     (50.40, 50.401075, 0.252004),
     (50.90, 50.907614, 0.254536),
     (51.40, 51.419244, 0.257095),
     (51.90, 51.936016, 0.259678),
     (52.50, 52.457981, 0.262288),
     (53.00, 52.985193, 0.264924),
     (53.50, 53.517703, 0.267587),
     (54.10, 54.055565, 0.270276),
     (54.60, 54.598832, 0.272992),
     (55.10, 55.147560, 0.275736),
     (55.70, 55.701802, 0.278507),
     (56.30, 56.261614, 0.281306),
     (56.80, 56.827053, 0.284133),
     (57.40, 57.398175, 0.286989),
     (58.00, 57.975036, 0.289873),
     (58.60, 58.557694, 0.292786),
     (59.10, 59.146209, 0.295729),
     (59.70, 59.740638, 0.298701),
     (60.30, 60.341042, 0.301703),
     (60.90, 60.947479, 0.304735),
     (61.60, 61.560012, 0.307798),
     (62.20, 62.178700, 0.310891),
     (62.80, 62.803606, 0.314015),
     (63.40, 63.434793, 0.317172),
     (64.10, 64.072323, 0.320359),
     (64.70, 64.716261, 0.323579),
     (65.40, 65.366670, 0.326831),
     (66.00, 66.023616, 0.330116),
     (66.70, 66.687164, 0.333433),
     (67.40, 67.357381, 0.336784),
     (68.00, 68.034334, 0.340169),
     (68.70, 68.718091, 0.343588),
     (69.40, 69.408719, 0.347041),
     (70.10, 70.106289, 0.350529),
     (70.80, 70.810869, 0.354052),
     (71.50, 71.522530, 0.357610),
     (72.20, 72.241343, 0.361204),
     (73.00, 72.967380, 0.364834),
     (73.70, 73.700715, 0.368501),
     (74.40, 74.441419, 0.372204),
     (75.20, 75.189568, 0.375945),
     (75.90, 75.945235, 0.379723),
     (76.70, 76.708498, 0.383540),
     (77.50, 77.479431, 0.387394),
     (78.30, 78.258113, 0.391288),
     (79.00, 79.044620, 0.395220),
     (79.80, 79.839031, 0.399192),
     (80.60, 80.641427, 0.403204),
     (81.50, 81.451886, 0.407256),
     (82.30, 82.270492, 0.411350),
     (83.10, 83.097324, 0.415483),
     (83.90, 83.932466, 0.419659),
     (84.80, 84.776001, 0.423876),
     (85.60, 85.628014, 0.428137),
     (86.50, 86.488590, 0.432440),
     (87.40, 87.357815, 0.436786),
     (88.20, 88.235775, 0.441175),
     (89.10, 89.122560, 0.445610),
     (90.00, 90.018257, 0.450088),
     (90.90, 90.922955, 0.454611),
     (91.80, 91.836746, 0.459180),
     (92.80, 92.759720, 0.463795),
     (93.70, 93.691971, 0.468456),
     (94.60, 94.633591, 0.473164),
     (95.60, 95.584675, 0.477920),
     (96.50, 96.545317, 0.482723),
     (97.50, 97.515613, 0.487574),
     (98.50, 98.495661, 0.492474),
     (99.50, 99.485559, 0.497424),
     (100.50, 100.485406, 0.5024),
     (101.50, 101.495301, 0.5074),
     (102.50, 102.515346, 0.5125),
     (103.50, 103.545642, 0.5177),
     (104.60, 104.586293, 0.5229),
     (105.60, 105.637403, 0.5281),
     (106.70, 106.699076, 0.5334),
     (107.80, 107.771420, 0.5388),
     (108.90, 108.854540, 0.5442),
     (109.90, 109.948547, 0.5497),
     (111.10, 111.053548, 0.5552),
     (112.20, 112.169655, 0.5608),
     (113.30, 113.296978, 0.5664),
     (114.40, 114.435632, 0.5721),
     (115.60, 115.585729, 0.5779),
     (116.70, 116.747385, 0.5837),
     (117.90, 117.920716, 0.5895),
     (119.10, 119.105839, 0.5955),
     (120.30, 120.302872, 0.6015),
     (121.50, 121.511936, 0.6075),
     (122.70, 122.733152, 0.6136),
     (124.00, 123.966640, 0.6198),
     (125.20, 125.212526, 0.6260),
     (126.50, 126.470933, 0.6323),
     (127.70, 127.741987, 0.6387),
     (129.00, 129.025815, 0.6451),
     (130.30, 130.322546, 0.6516),
     (131.60, 131.632309, 0.6581),
     (133.00, 132.955236, 0.6647),
     (134.30, 134.291458, 0.6714),
     (135.60, 135.641110, 0.6782),
     (137.00, 137.004326, 0.6850),
     (138.40, 138.381242, 0.6919),
     (139.80, 139.771997, 0.6988),
     (141.20, 141.176729, 0.7058),
     (142.60, 142.595578, 0.7129),
     (144.00, 144.028688, 0.7201),
     (145.50, 145.476200, 0.7273),
     (146.90, 146.938260, 0.7346),
     (148.40, 148.415014, 0.7420),
     (149.90, 149.906610, 0.7495),
     (151.40, 151.413197, 0.7570),
     (152.90, 152.934924, 0.7646),
     (154.50, 154.471946, 0.7723),
     (156.00, 156.024415, 0.7801),
     (157.60, 157.592486, 0.7879),
     (159.20, 159.176317, 0.7958),
     (160.80, 160.776066, 0.8038),
     (162.40, 162.391892, 0.8119),
     (164.00, 164.023958, 0.8201),
     (165.70, 165.672426, 0.8283),
     (167.30, 167.337461, 0.8366),
     (169.00, 169.019231, 0.8450),
     (170.70, 170.717902, 0.8535),
     (172.40, 172.433646, 0.8621),
     (174.20, 174.166633, 0.8708),
     (175.90, 175.917036, 0.8795),
     (177.70, 177.685032, 0.8884),
     (179.50, 179.470796, 0.8973),
]

dist_list=[x[0] for x in static_list]

movable_list=[
    (0.00, 0.026170, 0.026170),
    (0.10, 0.104789, 0.052450),
    (0.20, 0.208239, 0.051002),
    (0.30, 0.304589, 0.045349),
    (0.40, 0.411152, 0.061215),
    (0.50, 0.524658, 0.052292),
    (0.60, 0.607289, 0.030340),
    (0.70, 0.708214, 0.070587),
    (0.80, 0.819754, 0.040954),
    (0.90, 0.905969, 0.045262),
    (1.00, 1.001251, 0.050021),
    (1.10, 1.106553, 0.055282),
    (1.20, 1.222930, 0.061096),
    (1.30, 1.351546, 0.067521),
    (1.50, 1.493690, 0.074623),
    (1.60, 1.650783, 0.082471),
    (1.80, 1.824397, 0.091144),
    (2.00, 2.016270, 0.100731),
    (2.20, 2.228323, 0.111324),
    (2.50, 2.462678, 0.123032),
    (2.70, 2.721681, 0.135972),
    (3.00, 3.007922, 0.150271),
    (3.30, 3.324268, 0.166076),
    (3.70, 3.673884, 0.183542),
    (4.10, 4.060270, 0.202845),
    (4.50, 4.487293, 0.224179),
    (5.00, 4.959225, 0.247755),
    (5.50, 5.480791, 0.273812),
    (6.00, 6.057211, 0.302609),
    (6.70, 6.694254, 0.334435),
    (7.40, 7.398295, 0.369608),
    (8.20, 8.176380, 0.408479),
    (9.00, 9.036297, 0.451439),
    (10.00, 9.986652, 0.49891),
    (11.00, 11.036958, 0.5513),
    (12.20, 12.197725, 0.6093),
    (13.50, 13.480571, 0.6734),
    (14.90, 14.898335, 0.7442),
    (16.40, 16.465206, 0.8225),
    (18.20, 18.196867, 0.9090),
    (20.10, 20.110649, 1.0046),
    (22.20, 22.225705, 1.1103),
    (24.50, 24.563202, 1.2271),
    (27.10, 27.146537, 1.3561),
    (30.00, 30.001563, 1.4988),
    (33.10, 33.156855, 1.6564),
    (36.60, 36.643992, 1.8306),
    (40.40, 40.497874, 2.0232),
    (44.70, 44.757073, 2.2359),
    (49.40, 49.464215, 2.4711),
    (54.60, 54.666412, 2.7310),
    (60.30, 60.415729, 3.0182),
    (66.70, 66.769706, 3.3357),
    (73.70, 73.791938, 3.6865),
    (81.50, 81.552704, 4.0742),
    (90.00, 90.129676, 4.5027),
    (99.50, 99.608697, 4.9762),
    (109.90, 110.084635, 5.490),
    (121.50, 121.662337, 6.073),
    (134.30, 134.457677, 6.717),
    (148.40, 148.598714, 7.420),
    (164.00, 163.226977, 8.203),
    (181.30, 181.498879, 9.069),
    ]

def get_nearest(list,num):
    idx = np.abs(np.asarray(list)-num).argmin()
    return list[idx]

class WorldModel:
    """
    Holds and updates the model of the world as known from current and past
    data.
    """

    # constants for team sides
    SIDE_L = "l"
    SIDE_R = "r"


    class PlayModes:
        """
        Acts as a static class containing variables for all valid play modes.
        The string values correspond to what the referee calls the game modes.
        """
     

        BEFORE_KICK_OFF = "before_kick_off"
        PLAY_ON = "play_on"
        TIME_OVER = "time_over"
        KICK_OFF_L = "kick_off_l"
        KICK_OFF_R = "kick_off_r"
        KICK_IN_L = "kick_in_l"
        KICK_IN_R = "kick_in_r"
        FREE_KICK_L = "free_kick_l"
        FREE_KICK_R = "free_kick_r"
        CORNER_KICK_L = "corner_kick_l"
        CORNER_KICK_R = "corner_kick_r"
        GOAL_KICK_L = "goal_kick_l"
        GOAL_KICK_R = "goal_kick_r"
        DROP_BALL = "drop_ball"
        OFFSIDE_L = "offside_l"
        OFFSIDE_R = "offside_r"

        def __init__(self):
            raise NotImplementedError("Don't instantiate a PlayModes class,"
                    " access it statically through WorldModel instead.")

    class RefereeMessages:
        """
        Static class containing possible non-mode messages sent by a referee.
        """

        # these are referee messages, not play modes
        FOUL_L = "foul_l"
        FOUL_R = "foul_r"
        GOALIE_CATCH_BALL_L = "goalie_catch_ball_l"
        GOALIE_CATCH_BALL_R = "goalie_catch_ball_r"
        TIME_UP_WITHOUT_A_TEAM = "time_up_without_a_team"
        TIME_UP = "time_up"
        HALF_TIME = "half_time"
        TIME_EXTENDED = "time_extended"

        # these are special, as they are always followed by '_' and an int of
        # the number of goals scored by that side so far.  these won't match
        # anything specifically, but goals WILL start with these.
        GOAL_L = "goal_l_"
        GOAL_R = "goal_r_"

        def __init__(self):
            raise NotImplementedError("Don't instantiate a RefereeMessages class,"
                    " access it statically through WorldModel instead.")

    def __init__(self, action_handler):
        """
        Create the world model with default values and an ActionHandler class it
        can use to complete requested actions.
        """

        # we use the action handler to complete complex commands
        self.ah = action_handler

        # these variables store all objects for any particular game step
        self.ball = None
        self.flags = []
        self.goals = []
        self.players = []
        self.lines = []

        # the default position of this player, its home position
        self.home_point = (None, None)

        # scores for each side
        self.score_l = 0
        self.score_r = 0

        # the name of the agent's team
        self.teamname = None

        # handle player information, like uniform number and side
        self.side = None
        self.uniform_number = None

        # stores the most recent message heard
        self.last_message = None

        # the mode the game is currently in (default to not playing yet)
        self.play_mode = WorldModel.PlayModes.BEFORE_KICK_OFF

        # body state
        self.view_width = None
        self.view_quality = None
        self.stamina = None
        self.effort = None
        self.speed_amount = None
        self.speed_direction = None
        self.neck_direction = None

        # counts of actions taken so far
        self.kick_count = None
        self.dash_count = None
        self.turn_count = None
        self.say_count = None
        self.turn_neck_count = None
        self.catch_count = None
        self.move_count = None
        self.change_view_count = None

        # apparent absolute player coordinates and neck/body directions
        self.abs_coords = (None, None)
        self.abs_neck_dir = None
        self.abs_body_dir = None

        # absolute player position
        self.abs_pos = None
        self.abs_dir = None
        self.face_dir = None
        self.body_dir = None
        self.abs_vel_dir = None
        self.abs_vel_vec = None
        # create a new server parameter object for holding all server params
        self.server_parameters = ServerParameters()

    #
    def my_abs_pos(self, flags):
        # フラッグの静的位置を持ってくる
        flag_dict = game_object.Flag.FLAG_COORDS
        # seeメッセージで取れたフラッグを近い順にソート
        flags = sorted(flags, key=attrgetter('distance'))
        flag = flags[0]
        rel_pos = [0, 0]
        # フラッグの絶対方向はプレイヤーの首の絶対方向+フラッグの首からの相対方向
        flag_dir = self.face_dir + flag.direction
        # flag_dirを-180~180で正規化
        flag_dir = flag_dir % 360
        if flag_dir > 180:
            flag_dir = flag_dir - 360
        elif flag_dir < -180:
            flag_dir = flag_dir + 360
        # プレイヤーの相対位置を求める
        rel_pos[0] = flag.distance * math.cos(flag_dir * math.pi / 180)
        rel_pos[1] = flag.distance * math.sin(flag_dir * math.pi / 180)
        # プレイヤーの絶対位置を求める
        x = flag_dict[flag.flag_id][0] - rel_pos[0]
        y = flag_dict[flag.flag_id][1] - rel_pos[1]
        self.abs_pos = [x, y]
        return flag

    def my_err_pos(self, flags, iter=10):
        flag_dict = game_object.Flag.FLAG_COORDS
        flags = sorted(flags, key=attrgetter('distance'))
        dx,dy = [[],[]],[[],[]]
        flag = None
        for i in range(iter):
            try:
                flag = flags[i]

                flag_dir = self.face_dir + flag.direction

                # flag_dirを-180~180で正規化
                flag_dir = flag_dir % 360
                if flag_dir > 180:
                     flag_dir = flag_dir - 360
                elif flag_dir < -180:
                     flag_dir = flag_dir + 360

                flag_err = self.my_get_err(flag)
                dx[0].append(flag_dict[flag.flag_id][0]-((flag.distance - flag_err) * math.cos(flag_dir * math.pi / 180)))
                dx[1].append(flag_dict[flag.flag_id][0]-((flag.distance + flag_err) * math.cos(flag_dir * math.pi / 180)))
                dy[0].append(flag_dict[flag.flag_id][1]-((flag.distance - flag_err) * math.sin(flag_dir * math.pi / 180)))
                dy[1].append(flag_dict[flag.flag_id][1]-((flag.distance + flag_err) * math.sin(flag_dir * math.pi / 180)))
            except:
                pass
        if dx[0] < dx[1]:
            max_x = min(dx[1])
            min_x = min(dx[0])
        else:
            max_x = min(dx[0])
            min_x = min(dx[1])

        if dy[0] < dy[1]:
            max_y = min(dy[1])
            min_y = min(dy[0])
        else:
            max_y = min(dy[0])
            min_y = min(dy[1])
        ave_x = (max_x + min_x) * 0.5
        ave_y = (max_y + min_y) * 0.5

        self.abs_pos = [ave_x, ave_y]
        return flag

    def my_get_err(self, obj):
        dist = obj.distance
        static_list_idx = dist_list.index(get_nearest(dist_list, dist))
        obj_err = static_list[static_list_idx][2]
        return obj_err

    def my_abs_neck_dir(self, lines):
        if len(lines) >= 2:
            lines = sorted(lines, key=attrgetter('direction'))
        elif len(lines) == 1:
            pass
        else:
            print("cannnot calculate facedir")

        face_dir = lines[0].direction
        if face_dir < 0:
            face_dir += 90
        elif face_dir > 0:
            face_dir -= 90

        if lines[0].line_id == "l":
            face_dir = 180 - face_dir
        elif lines[0].line_id == "r":
            face_dir = 0 - face_dir
        elif lines[0].line_id == "t":
            face_dir = -90 - face_dir
        elif lines[0].line_id == "b":
            face_dir = 90 - face_dir

        if len(lines) >= 2:
            face_dir += 180

        face_dir = face_dir % 360.0
        if face_dir > 180:
            face_dir = face_dir - 360
        self.face_dir = face_dir
        return face_dir

    def my_abs_body_dir(self):
        self.body_dir = self.face_dir + self.neck_direction
        return self.body_dir

    def my_vel_vec(self):
        vector = [0,0]
        abs_vel_dir = self.face_dir + self.speed_direction
        vector[0] = self.speed_amount * math.cos(abs_vel_dir*math.pi/180)
        vector[1] = self.speed_amount * math.sin(abs_vel_dir*math.pi/180)
        self.abs_vel_vec = vector

    def my_obj_pos(self, obj):
        rel_pos = [0, 0]
        rel_pos[0] = obj.distance*math.cos((obj.direction+self.face_dir)*math.pi/180)
        rel_pos[1] = obj.distance*math.sin((obj.direction+self.face_dir)*math.pi/180)
        abs_obj_pos = [self.abs_pos[0]+rel_pos[0], self.abs_pos[1]+rel_pos[1]]
        return abs_obj_pos

    def my_obj_vel(self, obj):
        rel_vel = [0, 0]
        vec = [0, 0]
        if obj.dist_change is not None or obj.dir_change is not None:
            rel_vel[0] = obj.dist_change
            rel_vel[1] = obj.dir_change * obj.distance * (math.pi/180)
        rel_speed = math.sqrt(math.pow(rel_vel[0], 2) + math.pow(rel_vel[1], 2))
        if rel_vel[0] != 0:
            rotated_angle = math.atan(rel_vel[1]/rel_vel[0]) + (obj.dir + self.face_dir) * (math.pi/180)
        else:
            rotated_angle = 0
        vec[0] = rel_speed * math.cos(rotated_angle)
        vec[1] = rel_speed * math.sin(rotated_angle)
        return vec

    def triangulate_direction(self, flags, flag_dict):
        """
        Determines absolute view angle for the player given a list of visible
        flags.  We find the absolute angle to each flag, then return the average
        of those angles.  Returns 'None' if no angle could be determined.
        """

        # average all flag angles together and save that as absolute angle
        abs_angles = []

        for f in self.flags:
            # if the flag has useful data, consider it
            if f.distance is not None and f.flag_id in flag_dict:
                flag_point = flag_dict[f.flag_id]
                abs_dir = self.angle_between_points(self.abs_coords, flag_point)
                abs_angles.append(abs_dir)

        # return the average if available
        if len(abs_angles) > 0:
            return sum(abs_angles) / len(abs_angles)

        return None


    def triangulate_position(self, flags, flag_dict, angle_step=36):
        """
        Returns a best-guess position based on the triangulation via distances
        to all flags in the flag list given.  'angle_step' specifies the
        increments between angles for projecting points onto the circle
        surrounding a flag.
        """

        points = []
        for f in flags:
            # skip flags without distance information or without a specific id
            if f.distance is None or f.flag_id not in flag_dict:
                continue

            # generate points every 'angle_step' degrees around each flag,
            # discarding those off-field.
            for i in range(0, 360, angle_step):
                dy = f.distance * math.sin(math.radians(i))
                dx = f.distance * math.cos(math.radians(i))

                fcoords = flag_dict[f.flag_id]
                new_point = (fcoords[0] + dx, fcoords[1] + dy)

                # skip points with a coordinate outside the play boundaries
                if (new_point[0] > 60 or new_point[0] < -60 or
                        new_point[1] < -40 or new_point[1] > 40):
                    continue

                # add point to list of all points
                points.append(new_point)

        # get the dict of clusters mapped to centers
        clusters = self.cluster_points(points)

        # return the center that has the most points as an approximation to our
        # absolute position.
        center_with_most_points = (0, 0)
        max_points = 0
        for c in clusters:
            if len(clusters[c]) > max_points:
                center_with_most_points = c
                max_points = len(clusters[c])

        return center_with_most_points

    def cluster_points(self, points, num_cluster_iterations=15):
        """
        Cluster a set of points into a dict of centers mapped to point lists.
        Uses the k-means clustering algorithm with random initial centers and a
        fixed number of iterations to find clusters.
        """

        # generate initial random centers, ignoring identical ones
        centers = set([])
        for i in range(int(math.sqrt(len(points) / 2))):
            # a random coordinate somewhere within the field boundaries
            rand_center = (random.randint(-55, 55), random.randint(-35, 35))
            centers.add(rand_center)

        # cluster for some iterations before the latest result
        latest = {}
        cur = {}
        for i in range(num_cluster_iterations):
            # initialze cluster lists
            for c in centers:
                cur[c] = []

            # put every point into the list of its nearest cluster center
            for p in points:
                # get a list of (distance to center, center coords) tuples
                c_dists = [(self.euclidean_distance(c, p), c) for c in centers]

                # find the smallest tuple's c (second item)
                nearest_center = min(c_dists)[1]

                # add point to this center's cluster
                cur[nearest_center].append(p)

            # recompute centers
            new_centers = set([])
            for cluster in list(cur.values()):
                tot_x = 0
                tot_y = 0

                # remove empty clusters
                if len(cluster) == 0:
                    continue

                # generate average center of cluster
                for p in cluster:
                    tot_x += p[0]
                    tot_y += p[1]

                # get average center and add to new centers set
                ave_center = (tot_x / len(cluster), tot_y / len(cluster))
                new_centers.add(ave_center)

            # move on to next iteration
            centers = new_centers
            latest = cur
            cur = {}

        # return latest cluster iteration
        return latest

    def euclidean_distance(self, point1, point2):
        """
        Returns the Euclidean distance between two points on a plane.
        """

        try:
            x1 = point1[0]
            y1 = point1[1]
            x2 = point2[0]
            y2 = point2[1]
    
            return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        except:
            return 200

    def angle_between_points(self, point1, point2):
        """
        Returns the angle from the first point to the second, assuming that
        these points exist on a plane, and that the positive x-axis is 0 degrees
        and the positive y-axis is 90 degrees.  All returned angles are positive
        and relative to the positive x-axis.
        """

        try:
            x1 = point1[0]
            y1 = point1[1]
            x2 = point2[0]
            y2 = point2[1]

            # get components of vector between the points
            dx = x2 - x1
            dy = y2 - y1

            # return the angle in degrees
            a = math.degrees(math.atan2(dy, dx))
            if a < 0:
                a = 360 + a
    
            return a
        except:
            return 0

    def process_new_info(self, ball, flags, goals, players, lines):
        """
        Update any internal variables based on the currently available
        information.  This also calculates information not available directly
        from server-reported messages, such as player coordinates.
        """

        # update basic information
        self.ball = ball
        self.flags = flags
        self.goals = goals
        self.players = players
        self.lines = lines


        # update the apparent coordinates of the player based on all flag pairs
        face_dir = self.my_abs_neck_dir(self.lines)
        body_dir = self.my_abs_body_dir()
        flag = self.my_err_pos(self.flags)
        self.abs_coords = self.abs_pos

        # set the neck and body absolute directions based on flag directions
        self.abs_neck_dir = face_dir

        # set body dir only if we got a neck dir, else reset it
        if self.abs_neck_dir is not None:
            self.abs_body_dir = body_dir
        else:
            self.abs_body_dir = None

    def is_playon(self):
        """
        Tells us whether it's play time
        """
        return self.play_mode == WorldModel.PlayModes.PLAY_ON or self.play_mode == WorldModel.PlayModes.KICK_OFF_L or self.play_mode == WorldModel.PlayModes.KICK_OFF_R or self.play_mode == WorldModel.PlayModes.KICK_IN_L or self.play_mode == WorldModel.PlayModes.KICK_IN_R or self.play_mode == WorldModel.PlayModes.FREE_KICK_L or self.play_mode == WorldModel.PlayModes.FREE_KICK_R or self.play_mode == WorldModel.PlayModes.CORNER_KICK_L or self.play_mode == WorldModel.PlayModes.CORNER_KICK_R or self.play_mode == WorldModel.PlayModes.GOAL_KICK_L or self.play_mode == WorldModel.PlayModes.GOAL_KICK_R or self.play_mode == WorldModel.PlayModes.DROP_BALL or self.play_mode == WorldModel.PlayModes.OFFSIDE_L or self.play_mode == WorldModel.PlayModes.OFFSIDE_R

    def is_before_kick_off(self):
        """
        Tells us whether the game is in a pre-kickoff state.
        """

        return self.play_mode == WorldModel.PlayModes.BEFORE_KICK_OFF

    def is_kick_off_us(self):
        """
        Tells us whether it's our turn to kick off.
        """

        ko_left = WorldModel.PlayModes.KICK_OFF_L
        ko_right = WorldModel.PlayModes.KICK_OFF_R

        # print self.play_mode

        # return whether we're on the side that's kicking off
        return (self.side == WorldModel.SIDE_L and self.play_mode == ko_left or
                self.side == WorldModel.SIDE_R and self.play_mode == ko_right)

    def is_dead_ball_them(self):
        """
        Returns whether the ball is in the other team's posession and it's a
        free kick, corner kick, or kick in.
        """

        # shorthand for verbose constants
        kil = WorldModel.PlayModes.KICK_IN_L
        kir = WorldModel.PlayModes.KICK_IN_R
        fkl = WorldModel.PlayModes.FREE_KICK_L
        fkr = WorldModel.PlayModes.FREE_KICK_R
        ckl = WorldModel.PlayModes.CORNER_KICK_L
        ckr = WorldModel.PlayModes.CORNER_KICK_R

        # shorthand for whether left team or right team is free to act
        pm = self.play_mode
        free_left = (pm == kil or pm == fkl or pm == ckl)
        free_right = (pm == kir or pm == fkr or pm == ckr)

        # return whether the opposing side is in a dead ball situation
        if self.side == WorldModel.SIDE_L:
            return free_right
        else:
            return free_left

    def is_ball_kickable(self):
        """
        Tells us whether the ball is in reach of the current player.
        """

        # ball must be visible, not behind us, and within the kickable margin
        return (self.ball is not None and
                self.ball.distance is not None and
                self.ball.distance <= self.server_parameters.kickable_margin)

    def get_ball_speed_max(self):
        """
        Returns the maximum speed the ball can be kicked at.
        """

        return self.server_parameters.ball_speed_max

    def kick_to(self, point, extra_power=0.0):
        """
        Kick the ball to some point with some extra-power factor added on.
        extra_power=0.0 means the ball should stop at the given point, anything
        higher means it should have proportionately more speed.
        """

        # how far are we from the desired point?
        point_dist = self.euclidean_distance(self.abs_coords, point)

        # get absolute direction to the point
        abs_point_dir = self.angle_between_points(self.abs_coords, point)

        # get relative direction to point from body, since kicks are relative to
        # body direction.
        if self.abs_body_dir is not None:
            rel_point_dir = self.abs_body_dir - abs_point_dir

        # we do a simple linear interpolation to calculate final kick speed,
        # assuming a kick of power 100 goes 45 units in the given direction.
        # these numbers were obtained from section 4.5.3 of the documentation.
        # TODO: this will fail if parameters change, needs to be more flexible
        max_kick_dist = 45.0
        dist_ratio = point_dist / max_kick_dist

        # find the required power given ideal conditions, then add scale up by
        # difference bewteen actual aceivable power and maxpower.
        required_power = dist_ratio * self.server_parameters.maxpower
        effective_power = self.get_effective_kick_power(self.ball,
                required_power)
        required_power += 1 - (effective_power / required_power)

        # add more power!
        power_mod = 1.0 + extra_power
        power = required_power * power_mod

        # do the kick, finally
        self.ah.kick(rel_point_dir, power)

    def get_effective_kick_power(self, ball, power):
        """
        Returns the effective power of a kick given a ball object.  See formula
        4.21 in the documentation for more details.
        """

        # we can't calculate if we don't have a distance to the ball
        if ball.distance is None:
            return

        # first we get effective kick power:
        # limit kick_power to be between minpower and maxpower
        kick_power = max(min(power, self.server_parameters.maxpower),
                self.server_parameters.minpower)

        # scale it by the kick_power rate
        kick_power *= self.server_parameters.kick_power_rate

        # now we calculate the real effective power...
        a = 0.25 * (ball.direction / 180)
        b = 0.25 * (ball.distance / self.server_parameters.kickable_margin)

        # ...and then return it
        return 1 - a - b

    def turn_neck_to_object(self, obj):
        """
        Turns the player's neck to a given object.
        """

        self.ah.turn_neck(obj.direction)

    def get_distance_to_point(self, point):
        """
        Returns the linear distance to some point on the field from the current
        point.
        """

        return self.euclidean_distance(self.abs_coords, point)

    # Keng-added
    def get_angle_to_point(self, point):
        """
        Returns the relative angle to some point on the field from self.
        """

        # calculate absolute direction to point
        # subtract from absolute body direction to get relative angle
        return self.abs_body_dir - self.angle_between_points(self.abs_coords, point)

    # Keng-added
    def turn_body_to_point(self, point):
        """
        Turns the agent's body to face a given point on the field.
        """

        relative_dir = self.get_angle_to_point(point)

        if relative_dir > 180:
            relative_dir = relative_dir - 180
        elif relative_dir < -180:
            relative_dir = relative_dir + 180

        # turn to that angle
        self.ah.turn(relative_dir)

    def get_object_absolute_coords(self, obj):
        """
        Determines the absolute coordinates of the given object based on the
        agent's current position.  Returns None if the coordinates can't be
        calculated.
        """

        # we can't calculate this without a distance to the object
        if obj.distance is None:
            return None

        # get the components of the vector to the object
        dx = obj.distance * math.cos(obj.direction)
        dy = obj.distance * math.sin(obj.direction)

        # return the point the object is at relative to our current position
        return (self.abs_coords[0] + dx, self.abs_coords[1] + dy)

    def teleport_to_point(self, point):
        """
        Teleports the player to a given (x, y) point using the 'move' command.
        """

        self.ah.move(point[0], point[1])

    def align_neck_with_body(self):
        """
        Turns the player's neck to be in line with its body, making the angle
        between the two 0 degrees.
        """

        # neck angle is relative to body, so we turn it back the inverse way
        if self.neck_direction is not None:
            self.ah.turn_neck(self.neck_direction * -1)

    def get_nearest_teammate_to_point(self, point):
        """
        Returns the uniform number of the fastest teammate to some point.
        """

        # holds tuples of (player dist to point, player)
        distances = []
        for p in self.players:
            # skip enemy and unknwon players
            if p.side == self.side:
                # find their absolute position
                p_coords = self.get_object_absolute_coords(p)

                distances.append((self.euclidean_distance(point, p_coords), p))

        # return the nearest known teammate to the given point
        try:
            nearest = min(distances)[1]
            return nearest
        except:
            return None

    # Keng-added
    def get_nearest_teammate(self):
        """
        Returns the teammate player closest to self.
        """

        # holds tuples of (player dist to point, player)
        distances = []
        # print "checking from get_nearest_teammate"
        # print "selfside", self.side
        for p in self.players:
            # print p.side
            # print p.side == self.side
            # skip enemy and unknwon players
            if p.side == self.side:
                # find their absolute position
                p_coords = self.get_object_absolute_coords(p)

                distances.append((self.get_distance_to_point(p_coords), p))

        # print "finally", distances
        # return the nearest known teammate to the given point
        try:
            nearest = min(distances)[1]
            return nearest
        except:
            return None

    # Keng-added
    def get_nearest_enemy(self):
        """
        Returns the enemy player closest to self.
        """

        # holds tuples of (player dist to point, player)
        distances = []
        for p in self.players:
            # skip enemy and unknwon players
            if p.side != self.side:
                # find their absolute position
                p_coords = self.get_object_absolute_coords(p)

                distances.append((self.get_distance_to_point(p_coords), p))

        # return the nearest known teammate to the given point
        try:
            nearest = min(distances)[1]
            return nearest
        except:
            return None

    # Keng-added
    def is_ball_owned_by_us(self):
        """
        Returns if the ball is in possession by our team.
        """

        # holds tuples of (player dist to point, player)
        for p in self.players:
            # skip enemy and unknwon players
            if p.side == self.side and self.euclidean_distance(self.get_object_absolute_coords(self.ball), self.get_object_absolute_coords(p)) < self.server_parameters.kickable_margin:
                return True
            else:
                continue

        return False

    # Keng-added
    def is_ball_owned_by_enemy(self):
        """
        Returns if the ball is in possession by the enemy team.
        """

        # holds tuples of (player dist to point, player)
        for p in self.players:
            # skip enemy and unknwon players
            if p.side != self.side and self.euclidean_distance(self.get_object_absolute_coords(self.ball), self.get_object_absolute_coords(p)) < self.server_parameters.kickable_margin:
                return True
            else:
                continue

        return False

    def get_stamina(self):
        """
        Returns the agent's current stamina amount.
        """

        return self.stamina

    def get_stamina_max(self):
        """
        Returns the maximum amount of stamina a player can have.
        """

        return self.server_parameters.stamina_max

    def turn_body_to_object(self, obj):
        """
        Turns the player's body to face a particular object.
        """

        self.ah.turn(obj.direction)

class ServerParameters:
    """
    A storage container for all the settings of the soccer server.
    """


    def __init__(self):
        """
        Initialize default parameters for a server.
        """

        self.audio_cut_dist = 50
        self.auto_mode = 0
        self.back_passes = 1
        self.ball_accel_max = 2.7
        self.ball_decay = 0.94
        self.ball_rand = 0.05
        self.ball_size = 0.085
        self.ball_speed_max = 2.7
        self.ball_stuck_area = 3
        self.ball_weight = 0.2
        self.catch_ban_cycle = 5
        self.catch_probability = 1
        self.catchable_area_l = 2
        self.catchable_area_w = 1
        self.ckick_margin = 1
        self.clang_advice_win = 1
        self.clang_define_win = 1
        self.clang_del_win = 1
        self.clang_info_win = 1
        self.clang_mess_delay = 50
        self.clang_mess_per_cycle = 1
        self.clang_meta_win = 1
        self.clang_rule_win = 1
        self.clang_win_size = 300
        self.coach = 0
        self.coach_port = 6001
        self.coach_w_referee = 0
        self.connect_wait = 300
        self.control_radius = 2
        self.dash_power_rate =0.006
        self.drop_ball_time = 200
        self.effort_dec = 0.005
        self.effort_dec_thr = 0.3
        self.effort_inc = 0.01
        self.effort_inc_thr = 0.6
        self.effort_init = 1
        self.effort_min = 0.6
        self.forbid_kick_off_offside = 1
        self.free_kick_faults = 1
        self.freeform_send_period = 20
        self.freeform_wait_period = 600
        self.fullstate_l = 0
        self.fullstate_r = 0
        self.game_log_compression = 0
        self.game_log_dated = 1
        self.game_log_dir = './'
        self.game_log_fixed = 0
        self.game_log_fixed_name = 'rcssserver'
        self.game_log_version = 3
        self.game_logging = 1
        self.game_over_wait = 100
        self.goal_width = 14.02
        self.goalie_max_moves = 2
        self.half_time = 300
        self.hear_decay = 1
        self.hear_inc = 1
        self.hear_max = 1
        self.inertia_moment = 5
        self.keepaway = 0
        self.keepaway_length = 20
        self.keepaway_log_dated = 1
        self.keepaway_log_dir = './'
        self.keepaway_log_fixed = 0
        self.keepaway_log_fixed_name = 'rcssserver'
        self.keepaway_logging = 1
        self.keepaway_start = -1
        self.keepaway_width = 20
        self.kick_off_wait = 100
        self.kick_power_rate = 0.027
        self.kick_rand = 0
        self.kick_rand_factor_l = 1
        self.kick_rand_factor_r = 1
        self.kickable_margin = 0.7
        self.landmark_file = '~/.rcssserver-landmark.xml'
        self.log_date_format = '%Y%m%d%H%M-'
        self.log_times = 0
        self.max_goal_kicks = 3
        self.maxmoment = 180
        self.maxneckang = 90
        self.maxneckmoment = 180
        self.maxpower = 100
        self.minmoment = -180
        self.minneckang = -90
        self.minneckmoment = -180
        self.minpower = -100
        self.nr_extra_halfs = 2
        self.nr_normal_halfs = 2
        self.offside_active_area_size = 2.5
        self.offside_kick_margin = 9.15
        self.olcoach_port = 6002
        self.old_coach_hear = 0
        self.pen_allow_mult_kicks = 1
        self.pen_before_setup_wait = 30
        self.pen_coach_moves_players = 1
        self.pen_dist_x = 42.5
        self.pen_max_extra_kicks = 10
        self.pen_max_goalie_dist_x = 14
        self.pen_nr_kicks = 5
        self.pen_random_winner = 0
        self.pen_ready_wait = 50
        self.pen_setup_wait = 100
        self.pen_taken_wait = 200
        self.penalty_shoot_outs = 1
        self.player_accel_max = 1
        self.player_decay = 0.4
        self.player_rand = 0.1
        self.player_size = 0.3
        self.player_speed_max = 1.2
        self.player_weight = 60
        self.point_to_ban = 5
        self.point_to_duration = 20
        self.port = 6000
        self.prand_factor_l = 1
        self.prand_factor_r = 1
        self.profile = 0
        self.proper_goal_kicks = 0
        self.quantize_step = 0.1
        self.quantize_step_l = 0.01
        self.record_messages = 0
        self.recover_dec = 0.002
        self.recover_dec_thr = 0.3
        self.recover_init = 1
        self.recover_min = 0.5
        self.recv_step = 10
        self.say_coach_cnt_max = 128
        self.say_coach_msg_size = 128
        self.say_msg_size = 10
        self.send_comms = 0
        self.send_step = 150
        self.send_vi_step = 100
        self.sense_body_step = 100
        self.simulator_step = 100
        self.slow_down_factor = 1
        self.slowness_on_top_for_left_team = 1
        self.slowness_on_top_for_right_team = 1
        self.stamina_inc_max = 45
        self.stamina_max = 4000
        self.start_goal_l = 0
        self.start_goal_r = 0
        self.stopped_ball_vel = 0.01
        self.synch_micro_sleep = 1
        self.synch_mode = 0
        self.synch_offset = 60
        self.tackle_back_dist = 0.5
        self.tackle_cycles = 10
        self.tackle_dist = 2
        self.tackle_exponent = 6
        self.tackle_power_rate = 0.027
        self.tackle_width = 1
        self.team_actuator_noise = 0
        self.text_log_compression = 0
        self.text_log_dated = 1
        self.text_log_dir = './'
        self.text_log_fixed = 0
        self.text_log_fixed_name = 'rcssserver'
        self.text_logging = 1
        self.use_offside = 1
        self.verbose = 0
        self.visible_angle = 90
        self.visible_distance = 3
        self.wind_ang = 0
        self.wind_dir = 0
        self.wind_force = 0
        self.wind_none = 0
        self.wind_rand = 0
        self.wind_random = 0

        # add parameters by junichi
        self.pitch_width = 105.0
        self.pitch_length = 68.0
        self.pitch_margin = 5.0
        self.center_circle_r = 9.15
        self.penalty_area_length = 16.5
        self.penalty_area_width = 40.32
        self.penalty_area_circle = 9.15
        self.penalty_spot_dist = 11.0
        self.goal_area_length = 5.5
        self.goal_area_width = 18.32
        self.goal_depth = 2.44
        self.corner_arc_r = 1.0
        self.goal_post_radius = 0.06

    def get_pitch_width(self):
        return self.pitch_width

    def get_pitch_length(self):
        return self.pitch_length

    def get_penalty_area_length(self):
        return self.penalty_area_length

    def get_penalty_area_width(self):
        return self.penalty_area_width

    def get_goal_width(self):
        return self.goal_width



