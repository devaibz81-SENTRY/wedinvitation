/**
 * Google Apps Script - Wedding Songs & Messages
 * Deploy as Web App with "Anyone" access
 * Sheet needs 2 tabs: "Songs" and "Messages"
 * Columns: Timestamp, Name, Song/Message, Date
 */

function doGet(e) {
  const sheetName = e.parameter.sheet || 'Songs';
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({error: 'Sheet not found'}))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  const data = [];
  const values = sheet.getDataRange().getValues();
  
  // Skip header row
  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    data.push({
      timestamp: row[0],
      name: row[1],
      content: row[2], // Song or Message
      date: row[3]
    });
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    sheet: sheetName,
    count: data.length,
    data: data
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheetName = e.parameter.sheet || 'Songs';
  const sheet = ss.getSheetByName(sheetName);
  
  if (!sheet) {
    return ContentService.createTextOutput(JSON.stringify({error: 'Sheet not found'}))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  const payload = JSON.parse(e.postData.contents);
  const now = new Date();
  const dateStr = now.toLocaleDateString();
  
  sheet.appendRow([now, payload.name || 'Guest', payload.content || '', dateStr]);
  
  return ContentService.createTextOutput(JSON.stringify({success: true}))
    .setMimeType(ContentService.MimeType.JSON);
}
