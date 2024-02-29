import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://flooffy.mixlab.com/queue/confirm/readyToProcess');
  await page.goto('https://flooffy.mixlab.com/login');
  await page.getByLabel('Email').click();
  await page.getByLabel('Email').fill('aleks-test@mixlabrx.com');
  await page.getByLabel('Email').press('Tab');
  await page.getByLabel('Password').click();
  await page.getByLabel('Password').fill('VkN56bCaYv4b$p28&rr#EM');
  await page.getByRole('button', { name: 'Log in' }).click();
});