/**
 * Auth mock APIs including login, logout, invite, register
 */
import { rest } from 'msw';
import { BASE_URL, EMAIL_LOGIN_URL } from '../../constant/url';

export const loginMockService = rest.post(`${BASE_URL}${EMAIL_LOGIN_URL}`, async (req, res, ctx) => {
  const { email, password } = await req.json();
  if (email === 'user@example.com' && password === 'password') {
    return res(
      ctx.set('set-cookie', 'sdfhisdfhsfsfsdf'),
      ctx.json({
        data: {
          access_token: '12345678',
          refresh_token: '123456789',
        },
        msg: 'success',
        code: 200,
      })
    );
  } else {
    return res(
      ctx.status(401),
      ctx.json({
        data: {},
        msg: 'Incorrect password or Username',
      })
    );
  }
});

const authMockService = [loginMockService];

export default authMockService;
