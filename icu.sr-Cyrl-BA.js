(function() {

	var dfs = {"am_pm":["прије подне","по подне"],"day_name":["недјеља","понедељак","уторак","сриједа","четвртак","петак","субота"],"day_short":["нед.","пон.","ут.","ср.","чет.","пет.","суб."],"era":["п. н. е.","н. е."],"era_name":["прије нове ере","нове ере"],"month_name":["јануар","фебруар","март","април","мај","јун","јул","август","септембар","октобар","новембар","децембар"],"month_short":["јан.","феб.","март","апр.","мај","јун","јул","авг.","септ.","окт.","нов.","дец."],"order_full":"DMY","order_long":"DMY","order_medium":"YMD","order_short":"YMD"};
	var nfs = {"decimal_separator":",","grouping_separator":".","minus":"-"};
	var df = {SHORT_PADDED_CENTURY:function(d){if(d){return(d.getFullYear()+'-'+((d.getMonth()+101)+'').substring(1)+'-'+((d.getDate()+101)+'').substring(1));}},SHORT:function(d){if(d){return((d.getFullYear()+'').substring(2)+'-'+((d.getMonth()+101)+'').substring(1)+'-'+((d.getDate()+101)+'').substring(1));}},SHORT_NOYEAR:function(d){if(d){return(((d.getMonth()+101)+'').substring(1)+'-'+((d.getDate()+101)+'').substring(1));}},SHORT_NODAY:function(d){if(d){return((d.getFullYear()+'').substring(2)+'-'+((d.getMonth()+101)+'').substring(1));}},MEDIUM:function(d){if(d){return(d.getFullYear()+'-'+((d.getMonth()+101)+'').substring(1)+'-'+((d.getDate()+101)+'').substring(1));}},MEDIUM_NOYEAR:function(d){if(d){return(((d.getMonth()+101)+'').substring(1)+'-'+((d.getDate()+101)+'').substring(1));}},MEDIUM_WEEKDAY_NOYEAR:function(d){if(d){return(dfs.day_short[d.getDay()]+' '+((d.getMonth()+101)+'').substring(1)+'-'+((d.getDate()+101)+'').substring(1));}},LONG_NODAY:function(d){if(d){return(dfs.month_name[d.getMonth()]+' '+d.getFullYear()+'.');}},LONG:function(d){if(d){return(((d.getDate()+101)+'').substring(1)+'.'+' '+dfs.month_name[d.getMonth()]+' '+d.getFullYear()+'.');}},FULL:function(d){if(d){return(dfs.day_name[d.getDay()]+','+' '+((d.getDate()+101)+'').substring(1)+'.'+' '+dfs.month_name[d.getMonth()]+' '+d.getFullYear()+'.');}}};
	
	var icu = {};
	if (typeof window !== "undefined") {
		icu = window.icu = window.icu || {};
	}
		
	icu.getCountry = function() { return "BA" };
	icu.getCountryName = function() { return "Босна и Херцеговина" };
	icu.getDateFormat = function(formatCode) { var retVal = {}; retVal.format = df[formatCode]; return retVal; };
	icu.getDateFormats = function() { return df; };
	icu.getDateFormatSymbols = function() { return dfs; };
	icu.getDecimalFormat = function(places) { var retVal = {}; retVal.format = function(n) { var ns = n < 0 ? Math.abs(n).toFixed(places) : n.toFixed(places); var ns2 = ns.split('.'); s = ns2[0]; var d = ns2[1]; var rgx = /(\d+)(\d{3})/;while(rgx.test(s)){s = s.replace(rgx, '$1' + nfs["grouping_separator"] + '$2');} return (n < 0 ? nfs["minus"] : "") + s + nfs["decimal_separator"] + d;}; return retVal; };
	icu.getDecimalFormatSymbols = function() { return nfs; };
	icu.getIntegerFormat = function() { var retVal = {}; retVal.format = function(i) { var s = i < 0 ? Math.abs(i).toString() : i.toString(); var rgx = /(\d+)(\d{3})/;while(rgx.test(s)){s = s.replace(rgx, '$1' + nfs["grouping_separator"] + '$2');} return i < 0 ? nfs["minus"] + s : s;}; return retVal; };
	icu.getLanguage = function() { return "sr" };
	icu.getLanguageName = function() { return "српски" };
	icu.getLocale = function() { return "sr-Cyrl-BA" };
	icu.getLocaleName = function() { return "српски (ћирилица, Босна и Херцеговина)" };

	module.exports = icu;
})();