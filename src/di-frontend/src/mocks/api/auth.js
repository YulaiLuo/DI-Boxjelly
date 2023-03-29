/**
 * Auth mock APIs including login, logout, invite, register
 */
import { rest } from 'msw';

export const loginMockService = rest.post('/di_auth/login', async (req, res, ctx) => {
  const { email, password } = await req.json();
  if (email === 'user@example.com' && password === 'password') {
    return res(
      ctx.json({
        data: {
          access_token: '12345678',
          refresh_token: '123456789',
        },
        msg: 'success',
      })
    );
  } else {
    return res(
      ctx.json({
        data: {},
        msg: 'Incorrect password or Username',
      })
    );
  }
});

const authMockService = [loginMockService];

export default authMockService;