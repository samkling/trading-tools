//@version=5
// indicator("SamK_Indicator", shorttitle="SK", overlay=true, timeframe="", timeframe_gaps=true)
indicator("SamK_Indicator", shorttitle="SK", overlay=true)

ma(source, length, type) =>
    type == "SMA" ? ta.sma(source, length) :
     type == "EMA" ? ta.ema(source, length) :
     type == "SMMA (RMA)" ? ta.rma(source, length) :
     type == "WMA" ? ta.wma(source, length) :
     type == "VWMA" ? ta.vwma(source, length) :
     na

displayIndicators = "Display Indicators"
allMas_group = "All Timeframe MAs"
dmas_group = "Daily MAs"
indicators = "Indicators"

showChillax = input.bool(false, "Show Chillax", group = displayIndicators, inline = "row1") and (timeframe.isdaily or timeframe.isweekly)
only20ema = input.bool(false, "Only 20ema", group = displayIndicators, inline = "row1")
excludeDailyIntraday = input.bool(true, "Exclude Daily Intraday", group = dmas_group, inline = "row2")
showBB_SP = input.bool(false, "Show BB SP", group = indicators, inline = "row1") and timeframe.isdaily
showADR = input.bool(true, "Show ADR", group = indicators, inline = "row1") and (timeframe.isdaily or timeframe.isweekly)
screenshot = input.bool(false, "Screenshot", group = indicators, inline = "row1") and (timeframe.isdaily or timeframe.isweekly)

showMAs = input.bool(true, "Show MAs All TF", group = allMas_group, inline = "50_200") and (not only20ema) and (not showBB_SP)
showDMAs = input.bool(false, "Show Daily MAs", group = dmas_group, inline = "row2") and (timeframe.isintraday or (not showMAs and timeframe.isdaily)) and (not only20ema) and (not excludeDailyIntraday) and (not showBB_SP)

show_50 = (input.bool(false, "Show 50sma", group = allMas_group, inline ="50_200" ) and (not only20ema) and (showMAs) and (timeframe.isdaily or timeframe.isweekly) ) or screenshot
show_100 = (input.bool(false, "Show 100sma", group = allMas_group, inline ="50_200" ) and (not only20ema) and (showMAs) and (timeframe.isdaily or timeframe.isweekly)) or screenshot
show_200 = (input.bool(false, "Show 200sma", group = allMas_group, inline ="50_200" ) and (not only20ema) and (showMAs) and (timeframe.isdaily or timeframe.isweekly)) or screenshot

showOops = input.bool(true, "Show Oops", group = displayIndicators, inline ="oops") and timeframe.isdaily
showOopsFail = input.bool(false, "Show Oops Fail", group = displayIndicators, inline ="oops") and timeframe.isdaily
showQQQ20 = input.bool(true, "Show QQQ20", group = displayIndicators, inline = "row1") and (timeframe.isdaily)
showRSI = input.bool(false, "Show W RSI", group = indicators, inline="RSI") and timeframe.isdaily


show_ma1_day   = input(true   , "MA Day №1", inline="MA Day #1", group = dmas_group) and showDMAs
ma1_day_type   = input.string("EMA"  , ""     , inline="MA Day #1", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group = dmas_group)
ma1_day_source = request.security(syminfo.ticker,"D",close)
ma1_day_length = input.int(10     , ""     , inline="MA Day #1", minval=1, group = dmas_group)
ma1_day_color  = input(color.fuchsia, ""     , inline="MA Day #1", group = dmas_group)
// ma1_day = ma(ma1_day_source, ma1_day_length, ma1_day_type)
ma1_day = request.security(syminfo.tickerid, "D", ma(ma1_day_source, ma1_day_length, ma1_day_type),lookahead = barmerge.lookahead_off, gaps=barmerge.gaps_on)
plot(show_ma1_day ? ma1_day : na, color = ma1_day_color, title="MA Day №1", linewidth = 2)

show_ma2_day   = input(true   , "MA Day №2", inline="MA Day №2", group = dmas_group) and showDMAs or (only20ema and not excludeDailyIntraday)
ma2_day_type   = input.string("EMA"  , ""     , inline="MA Day №2", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group = dmas_group)
ma2_day_source = request.security(syminfo.ticker,"D",close)
ma2_day_length = input.int(20     , ""     , inline="MA Day №2", minval=1, group = dmas_group)
ma2_day_color  = input(color.yellow, ""     , inline="MA Day №2", group = dmas_group)
// ma2_day = ma(ma2_day_source, ma2_day_length, ma2_day_type)
ma2_day = request.security(syminfo.tickerid, "D", ma(ma2_day_source, ma2_day_length, ma2_day_type),lookahead = barmerge.lookahead_off, gaps=barmerge.gaps_on)
plot(show_ma2_day ? ma2_day : na, color = ma2_day_color, title="MA Day №2", linewidth = 2)

show_ma1   = input(true   , "MA №1", inline="MA #1", group = allMas_group) and showMAs
ma1_type   = input.string("EMA"  , ""     , inline="MA #1", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group = allMas_group)
ma1_source = input(close  , ""     , inline="MA #1", group = allMas_group)
ma1_length = input.int(10     , ""     , inline="MA #1", minval=1, group = allMas_group)
ma1_color  = input(color.fuchsia, ""     , inline="MA #1", group = allMas_group)
ma1 = ma(ma1_source, ma1_length, ma1_type)
plot(show_ma1 ? ma1 : na, color = ma1_color, title="MA №1", linewidth = 2)

show_ma2   = input(true   , "MA №2", inline="MA #2", group = allMas_group) and showMAs or only20ema
ma2_type   = input.string("EMA"  , ""     , inline="MA #2", options=["SMA", "EMA", "SMMA (RMA)", "WMA", "VWMA"], group = allMas_group)
ma2_source = input(close  , ""     , inline="MA #2", group = allMas_group)
ma2_length = input.int(20     , ""     , inline="MA #2", minval=1, group = allMas_group)
ma2_color  = input(color.yellow, ""     , inline="MA #2", group = allMas_group)
ma2 = ma(ma2_source, ma2_length, ma2_type)
plot(show_ma2 ? ma2 : na, color = ma2_color, title="MA №2", linewidth = 2)

show_ma3   = showMAs and show_50
ma3_type   = "SMA"
ma3_source = close
ma3_length = 50
ma3_color  = color.aqua
ma3 = ma(ma3_source, ma3_length, ma3_type)
plot(show_ma3 ? ma3 : na, color = ma3_color, title="MA №3", linewidth = 2)

show_ma4   = showMAs and show_200
ma4_type = "SMA"
ma4_source = close
ma4_length = 200
ma4_color  = color.red
ma4 = ma(ma4_source, ma4_length, ma4_type)
plot(show_ma4 ? ma4 : na, color = ma4_color, title="MA №4", linewidth = 2)

show_ma5   = showMAs and show_100
ma5_type = "SMA"
ma5_source = close
ma5_length = 100
ma5_color  = color.green
ma5 = ma(ma5_source, ma5_length, ma5_type)
plot(show_ma5 ? ma5 : na, color = ma5_color, title="MA №5", linewidth = 2)

qqqPrice = request.security("QQQ", "D", close)
plotQQQ20 = showQQQ20 and (ta.ema(qqqPrice,20) < qqqPrice)
plotQ20I = (ta.ema(qqqPrice,20) < qqqPrice)
// plotshape(plotQQQ20, style = shape.square, color = color.rgb(30, 18, 204), location = location.bottom)

// below10 = ta.ema(close, 10) > open and plotQQQ20
// below10 = true

oopsReversal = (low[1] > open) and (high > low[1]) and showOops
oopsFail = (low[1] > open) and (high > low[1]) and (close < low[1]) and showOopsFail
plotshape(oopsReversal, style=shape.triangleup, location = location.bottom, color=color.lime)
plotshape(oopsFail, style=shape.xcross, location = location.bottom, color=color.red)

w_rsi = ta.rsi(close,14)
rsi_input = input.int(65, "RSI threshold", group = indicators, inline="RSI")
w = request.security(syminfo.ticker, "W", w_rsi)
plot_rsi = w > rsi_input and showRSI
plotshape(plot_rsi, style=shape.arrowup, location = location.bottom, color = color.gray, size = size.small)

plot(show_ma2 ? ma2 : na, color = plotQQQ20 ? color.lime : color.yellow, title="MA №2", linewidth = 2)
plot(show_ma2_day ? ma2_day : na, color = plotQ20I ? color.lime : color.yellow, title="MA Day №2", linewidth = 2)


length = 20
src1 = close
stdDev_1 = 1.0
stdDev_2 = 2.0
basis = ta.sma(src1, length)
dev_1 = stdDev_1 * ta.stdev(src1, length)
dev_2 = stdDev_2 * ta.stdev(src1, length)
upper_1 = basis + dev_1
upper_2 = basis + dev_2
lower_1 = basis - dev_1
lower_2 = basis - dev_2
offset = 0

// plot(basis, "Basis", color=#FF6D00, offset = offset)
plot(showBB_SP ? upper_1 : na, "Upper_1", color=color.blue, offset = offset,linewidth = 3)
plot(showBB_SP ? upper_2 : na, "Upper_2", color=color.gray, offset = offset)
plot(showBB_SP ? lower_1 : na, "Lower_1", color=color.blue, offset = offset,linewidth = 3)
plot(showBB_SP ? lower_2 : na, "Upper_2", color=color.gray, offset = offset)


// We use `var` to only initialize the table on the first bar.
var table atrDisplay = table.new(position.top_right,2,2)
// We call `ta.atr()` outside the `if` block so it executes on each bar.
// myAtr = math.round((ta.atr(14) / close)* 1000)/10
Length = (20)
dhigh = request.security(syminfo.tickerid, "D", high)
dlow = request.security(syminfo.tickerid, "D", low)
myAtr = 100 * (ta.sma(dhigh / dlow, Length) - 1)
avgVol = ma(volume, 50, "SMA")
rVol = volume/avgVol
if barstate.islast and showADR
    // We only populate the table on the last bar.
    table.cell(atrDisplay, 1, 1, "ADR: " + str.tostring(myAtr,"0.00") + "%",text_color = myAtr > 3.4 ? color.lime : color.red)
if showADR
    table.cell(atrDisplay, 0, 0, "V: " + str.tostring(volume/1000000,"0.00") + "m",text_color = close > close[1] ? color.lime : color.red)
    table.cell(atrDisplay, 1, 0, "VAv: " + str.tostring(avgVol/1000000,"0.00") + "m",text_color = color.yellow)
    table.cell(atrDisplay, 0, 1, "Rv: " + str.tostring(rVol,"0.0"),text_color = rVol > 1 ? color.lime : color.gray)

// yourmama = input.string(title='', options=['SMA', 'EMA'], defval='SMA', group='Moving Averages Type')

// ma(ma1_day_source, ma1_day_length, ma1_day_type)
//chillax

chillax = 'Chillax Settings'

ma1cl = input(10, title="First MA length", group = chillax, inline="row1")
src1cl = close
out1 = timeframe.isdaily ? ma(src1cl, ma1cl,'SMA') : timeframe.isweekly ? ma(src1cl, ma1cl,'EMA') : na

ma2cl = input(20, title="Second MA length", group = chillax, inline = "row1")
src2 = close
out2 = timeframe.isdaily ? ma(src2, ma2cl,'SMA') : timeframe.isweekly ? ma(src2, ma2cl,'EMA') : na


// plot(out1, color=color.red)
// plot(out2, color=color.black)

// the number of bars to determine uptrend, if trendlen is 5, and if today's ma is higher than 5 days ago's ma, then it is an uptrend
trendlen = input(5, title="number of bars to determine uptrend", group = chillax, inline = "row2")


over = out1 > out2 
out1up = out1 > out1[trendlen]
out2up = out2 > out2[trendlen] 

green = out1 > out2 and out1up and out2up
lightgreen = out1 > out2 and out1up and not out2up
yellow = out1 > out2 and not out1up and not out2up

bgColor = showChillax ? (green ? color.new(color.rgb(0, 150, 0), 50) : lightgreen ? color.new(color.rgb(0, 255, 0), 80) : yellow ? color.new(color.yellow, 80) : na) : na
   
bgcolor(color=bgColor)
