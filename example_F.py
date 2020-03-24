import statApi
from api import Api
mlApi = Api()

# define dataset specifics
filename = "../master-thesis-db/datasets/F/data2_30min.csv"

columns = [
	['FYN0111', 'Gasseksport rate', 'MSm^3/d'],
	['FT0111', 'Gasseksport molvekt','g/mole'],
	['TT0102_MA_Y', 'Varm side A temperatur inn', 'degrees'],
	['TIC0101_CA_YX', 'Varm side A temperatur ut', 'degrees'],
	['TT0104_MA_Y', 'Varm side B temperatur inn', 'degrees'],
	['TIC0103_CA_YX', 'Varm side B temperatur ut', 'degrees'],
	['TT0106_MA_Y', 'Varm side C temperatur inn', 'degrees'],
	['TIC0105_CA_YX', 'Varm side C temperatur ut', 'degrees'],
	['TI0115_MA_Y', 'Scrubber temperatur ut', 'degrees'],
	['PDT0108_MA_Y', 'Varm side A trykkfall', 'Bar'],
	['PDT0119_MA_Y', 'Varm side B trykkfall', 'Bar'],
	['PDT0118_MA_Y', 'Varm side C trykkfall', 'Bar'],
	['PIC0104_CA_YX', 'Innløpsseparator trykk', 'Barg'],
	['TIC0425_CA_YX', 'Kald side temperatur inn', 'degrees'],
	['TT0651_MA_Y', 'Kald side A temperatur ut', 'degrees'],
	['TT0652_MA_Y', 'Kald side B temperatur ut', 'degrees'],
	['TT0653_MA_Y', 'Kald side C temperatur ut', 'degrees'],
	['TIC0101_CA_Y', 'Kald side A ventilåpning', '%'],
	['TIC0103_CA_Y', 'Kald side B ventilåpning', '%'],
	['TIC0105_CA_Y', 'Kald side C ventilåpning', '%'],
]

irrelevantColumns = [
		'FT0111',
		'PDT0108_MA_Y',
		'PDT0119_MA_Y',
		'PDT0118_MA_Y',
		'TT0104_MA_Y',
		'TIC0103_CA_YX',
		'TI0115_MA_Y',
		'TT0652_MA_Y',
		'TIC0103_CA_Y',
		'PIC0104_CA_YX',
		'TIC0101_CA_Y',
		'TIC0105_CA_Y',
		'TT0102_MA_Y',
		'TIC0101_CA_YX',
		'TT0651_MA_Y',
]

targetColumns = [
    'TT0653_MA_Y'
]

traintime = [
        ["2017-08-05 00:00:00", "2018-08-01 00:00:00"],
    ]

testtime = [
    "2017-08-05 00:00:00",
    "2019-05-01 00:00:00"
]

df = mlApi.initDataframe(filename, columns, irrelevantColumns)
df_train, df_test = mlApi.getTestTrainSplit(traintime, testtime)
X_train, y_train, X_test, y_test = mlApi.getFeatureTargetSplit(targetColumns)

covmat = statApi.correlationMatrix(df_train)
statApi.printCorrelationMatrix(covmat, df_train, mlApi.columnDescriptions)

pca = statApi.pca(df_train, -1, mlApi.relevantColumns, mlApi.columnDescriptions)
statApi.printExplainedVarianceRatio(pca)
"""
statApi.pcaPlot(df, [traintime, testtime, []])

statApi.pairplot(df)

statApi.scatterplot(df)

statApi.correlationPlot(df_train)

statApi.valueDistribution(df, traintime, testtime)

"""

linear = mlApi.Linear('linear')
linear_r = mlApi.Linear_Regularized('linear r')

mlp_1x_128 = mlApi.MLP('mlp 1x 128', layers=[128])
mlpd_1x_128 = mlApi.MLP('mlpd 1x 128', layers=[128], dropout=0.2)
mlpr_1x_128 = mlApi.MLP('mlpr 1x 128', layers=[128], l1_rate=0.01, l2_rate=0.01)

lstm_1x_128 = mlApi.LSTM('lstm 1x 128', layers=[128])
lstmd_1x_128 = mlApi.LSTM('lstmr 1x 128', layers=[128], dropout=0.2, recurrentDropout=0.2)
lstmdx_1x_128 = mlApi.LSTM('lstmr 1x 128 no valve', layers=[128], dropout=0.2, recurrentDropout=0.2)
lstmdxx_1x_128 = mlApi.LSTM('lstmr 1x 128 no xxx', layers=[128], dropout=0.2, recurrentDropout=0.2)

modelList = [
	#mlpd_1x_128,
	#lstmd_1x_128,
	lstmdxx_1x_128,
	#lstmd_1x_128,
	#mlp_1x_128,
	#mlpd_1x_128,
	#mlpr_1x_128,
	#linear,
	#linear_r,
]

mlApi.initModels(modelList)
retrain=False
mlApi.trainModels(retrain)

import src.utils.modelFuncs as mf

"""
for model in modelList:
	print(model.name)
	mf.printModelSummary(model)
	print("")
	print("")
"""
#mlApi.predictWithAutoencoderModels()
modelNames, metrics_train, metrics_test = mlApi.predictWithModels(plot=True, interpol=False)

