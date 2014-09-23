/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
     config.extraPlugins = 'codemirror';
     config.fullPage = true;
     config.startupMode = 'source';
     config.codemirror = {
         theme:'blackboard',
         lineNumbers:true,
         lineWrapping:false,
         autoCloseBrackets:false,
         mode: {name: "jinja2",
               version: 2,
               singleLineStringErrors: false},
         showSearchButton:false,
         highlightActiveLine: false
     }


};
