const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs').promises;
const winston = require('winston');

// Configuração do logger com winston
const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'error' : 'debug',
  format: winston.format.combine(
    winston.format.colorize(),
    winston.format.timestamp(),
    winston.format.printf(({ timestamp, level, message }) => `${timestamp} [${level}]: ${message}`),
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log' }),
  ],
});

// Função auxiliar para executar comandos do sistema operacional
function executeCommand(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        logger.error(`Erro ao executar comando: ${stderr}`);
        reject(new Error(`Erro ao executar comando: ${stderr}`));
      } else {
        logger.debug(`Comando executado com sucesso: ${stdout}`);
        resolve(stdout);
      }
    });
  });
}

// Criação da janela principal
function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'renderer.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  mainWindow.loadFile('index.html');
}

// Eventos do Electron
app.on('ready', createWindow);
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Manipulador para seleção de arquivos
ipcMain.handle('select-file', async () => {
  try {
    const result = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [{ name: 'Planilhas e PDFs', extensions: ['xlsx', 'pdf'] }],
    });

    if (result.canceled || !result.filePaths.length) {
      throw new Error('Nenhum arquivo foi selecionado.');
    }

    const filePath = result.filePaths[0];

    // Verifica se o arquivo realmente existe
    await fs.access(filePath);
    logger.debug(`Arquivo selecionado: ${filePath}`);
    return filePath;
  } catch (error) {
    logger.error(`Erro ao selecionar o arquivo: ${error.message}`);
    throw new Error('Erro ao selecionar o arquivo. Verifique se ele existe e tente novamente.');
  }
});

// Manipulador para processar o arquivo localmente
ipcMain.handle('process-file', async (event, filePath) => {
  try {
    // Verifica novamente se o arquivo existe antes de processar
    await fs.access(filePath);

    const command = `python app/process_file.py "${filePath}"`;
    const result = await executeCommand(command);
    logger.debug(`Arquivo processado com sucesso: ${filePath}`);
    return result;
  } catch (error) {
    logger.error(`Erro ao processar o arquivo: ${error.message}`);
    throw new Error('Erro ao processar o arquivo. Verifique o caminho e tente novamente.');
  }
});
