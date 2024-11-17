const express = require('express');
const dotenv = require('dotenv');
const { getDiscordAuthUrl, getDiscordToken, getDiscordUserInfo } = require('./authController');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8080;

app.get('/get-url', (req, res) => {
    res.send({ url: getDiscordAuthUrl() });
});

app.get('/code-to-user', async (req, res) => {
    const { code } = req.query;
    if (!code) {
        return res.status(400).send('Missing code');
    }

    const token = await getDiscordToken(code);
    const userInfo = await getDiscordUserInfo(token);
    res.send(userInfo);
});

app.listen(PORT, () => console.log(`Сервис авторизации через Discord работает на порту ${PORT}`));