import { expect, test } from "@playwright/test";

test("shows the operational workbench shell", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByText("Research control room")).toBeVisible();
  await expect(page.getByRole("link", { name: "Data Intake" })).toBeVisible();
});