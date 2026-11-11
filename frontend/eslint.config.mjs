import { defineConfig } from "eslint/config";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";
import storybook from "eslint-plugin-storybook";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default defineConfig([
  ...compat.extends("next/core-web-vitals"),
  ...storybook.configs["flat/recommended"],
  {
    ignores: [".next/**", "storybook-static/**", "!.storybook"],
  },
  {
    rules: {
      "@next/next/no-img-element": "off",
    },
  },
]);
