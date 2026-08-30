const {getHooks: getProgramHooks} = require('@diplodoc/cli/lib/program');
const {getHooks: getMarkdownHooks} = require('@diplodoc/cli/lib/markdown');
const {transform} = require('@diplodoc/mermaid-extension');

/**
 * Adapts Mermaid's Markdown-It transformer to the Diplodoc extension API.
 * The adapter remains local; rendering is provided by the official package.
 */
class Extension {
  constructor(options = {}) {
    this.options = options;
  }

  apply(program) {
    getProgramHooks(program).BeforeAnyRun.tap('Mermaid', (run) => {
      getMarkdownHooks(run.markdown).Plugins.tap('Mermaid', (plugins) => {
        plugins.push(transform(this.options));
        return plugins;
      });
    });
  }
}

module.exports = {Extension};
