module.exports = {
  extends: 'airbnb-base',
  parser: '@babel/eslint-parser',
  parserOptions: {
    requireConfigFile: false,
  },
  rules: {
    'no-param-reassign': 0,
    'import/no-extraneous-dependencies': 0,
    'import/prefer-default-export': 0,
    'consistent-return': 0,
    'no-confusing-arrow': 0,
    'no-underscore-dangle': 0,
    'object-curly-newline': [
      'error',
      {
        ObjectExpression: { multiline: true, consistent: true },
        ObjectPattern: { multiline: true, consistent: true },
        ImportDeclaration: { multiline: true, consistent: true },
        ExportDeclaration: { multiline: true, consistent: true },
      },
    ],
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    'arrow-body-style': ['error', 'as-needed'],
    'prefer-promise-reject-errors': ['error', { allowEmptyReject: true }],
    'import/no-unresolved': ['error', { ignore: ['electron'] }],
  },
  env: {
    browser: true,
    node: true,
  },
  globals: {
    __dirname: true,
    jQuery: true,
    $: true,
  },
};
