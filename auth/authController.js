const axios = require('axios');
require('dotenv').config();

const DISCORD_OAUTH_URL = 'https://discord.com/api/oauth2/authorize';
const DISCORD_TOKEN_URL = 'https://discord.com/api/oauth2/token';
const DISCORD_USER_URL = 'https://discord.com/api/users/@me';

const getDiscordAuthUrl = () => {
    const params = new URLSearchParams({
        client_id: process.env.DISCORD_CLIENT_ID,
        redirect_uri: process.env.DISCORD_REDIRECT_URI,
        response_type: 'code',
        scope: 'identify',
    });

    return `${DISCORD_OAUTH_URL}?${params.toString()}`;
};

const getDiscordToken = async (code) => {
    const params = new URLSearchParams({
        client_id: process.env.DISCORD_CLIENT_ID,
        client_secret: process.env.DISCORD_CLIENT_SECRET,
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: process.env.DISCORD_REDIRECT_URI,
    });

    try {
        const { data } = await axios.post(DISCORD_TOKEN_URL, params);
        return data.access_token;
    } catch (err) {
        console.error('Ошибка авторизации Discord:', err.message);
    }
};

const getDiscordUserInfo = async (token) => {
    try {
        const { data } = await axios.get(DISCORD_USER_URL, {
            headers: { Authorization: `Bearer ${token}` },
        });
        return data;
    } catch (err) {
        console.error('Ошибка Discord:', err.message);
    }
};

module.exports = {
    getDiscordAuthUrl,
    getDiscordToken,
    getDiscordUserInfo,
};
