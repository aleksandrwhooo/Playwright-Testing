import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://flooffy.mixlab.com/');
  await page.goto('https://flooffy.mixlab.com/login');
  await page.getByLabel('Email').click();
  await page.getByLabel('Email').fill('aleks-test@mixlabrx.com');
  await page.getByLabel('Password').click();await page.getByLabel('Password').click();
  await page.getByLabel('Password').fill('VkN56bCaYv4b$p28&rr#EM');
  await page.getByRole('button', { name: 'Log in' }).click();
  await page.getByRole('button', { name: 'Scan bin' }).click();
});

// await page.getByTestId('popup-container').locator('a').first().click();
// await page.getByRole('link', { name: 'Queue' }).click();
// await page.getByRole('link', { name: 'Ready to process 46', exact: true }).click();