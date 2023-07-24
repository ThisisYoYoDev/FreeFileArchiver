const express = require('express');
const axios = require('axios');
const multer = require('multer');
const FormData = require('form-data');

const { webhook, port, max_file_size_in_mb, max_total_size, avatar_url } = require('../config/config.json');

const MAX_FILE_SIZE = (max_file_size_in_mb * 1024 * 1024) - 1;

const storage = multer.memoryStorage();
const upload = multer({ storage, limits: { fileSize: max_total_size } }).any();

const serverApp = express();

serverApp.get('/', (req, res) => {
    res.send({ success: true });
});

const getMaxFileSizeErrorMessage = (fileName, maxSize) => {
    return `File ${fileName} exceeds the maximum allowed size of ${Math.floor(maxSize / 1024 / 1024)} MB`;
};

serverApp.post('/upload', upload, async (req, res) => {
    const files = req.files ?? [];

    if (files.length === 0) {
        res.status(400).send({ error: 'No files provided' });
        return;
    }

    const fileTooLarge = files.find(file => file.size > MAX_FILE_SIZE);
    if (fileTooLarge) {
        res.status(400).send({ error: getMaxFileSizeErrorMessage(fileTooLarge.originalname, MAX_FILE_SIZE) });
        return;
    }

    const totalSize = files.reduce((total, file) => total + file.size, 0);

    if (totalSize > MAX_FILE_SIZE) {
        const fileParts = [];
        let currentPart = [];
        let currentPartSize = 0;

        for (const file of files) {
            if (currentPartSize + file.size > MAX_FILE_SIZE) {
                fileParts.push(currentPart);
                currentPart = [];
                currentPartSize = 0;
            }

            currentPart.push(file);
            currentPartSize += file.size;
        }

        if (currentPart.length > 0) {
            fileParts.push(currentPart);
        }

        const urls = [];

        try {
            const promises = fileParts.map(partFiles => sendfile(partFiles));
            const partUrlsArray = await Promise.all(promises);

            for (const partUrls of partUrlsArray) {
                if (partUrls.error) {
                    res.status(500).send({ error: partUrls.error });
                    return;
                }
                urls.push(...partUrls);
            }

            res.send({ urls });
        } catch (error) {
            res.status(500).send({ error: 'An error occurred during file processing' });
        }

    } else {
        try {
            const urls = await sendfile(files);
            if (urls.error) {
                res.status(500).send({ error: urls.error });
                return;
            }
            res.send({ urls });
        } catch (error) {
            res.status(500).send({ error: 'An error occurred during file processing' });
        }
    }
});

serverApp.listen(port, () => {
    console.info('Server is running on port', port);
});

async function sendfile(files) {
    const data = new FormData();
    data.append(
        "payload_json",
        `{"content":null,"embeds":null,"username":"File Archiver","avatar_url": "${avatar_url}"}`
    );

    files.forEach((file, i) => {
        data.append(`file[${i}]`, file.buffer, file.originalname);
    });


    return axios({
        method: "post",
        url: webhook,
        headers: data.getHeaders(),
        data,
    })
        .then(response => {
            const attachments = response.data.attachments;
            const urls = attachments.map(attachment => attachment.url);
            return urls;
        })
        .catch(error => {
            console.error(error);
            return { error: error.response.data.message };
        });
}