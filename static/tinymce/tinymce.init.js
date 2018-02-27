function tinymce_init() {
    tinymce.init({
      selector: 'textarea.vLargeTextField',
      height: 500,
      theme: 'modern',
      plugins: 'print fullpage searchreplace autolink directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount imagetools  contextmenu colorpicker textpattern code',
      toolbar1: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent  | fullscreen code removeformat',
      image_advtab: true,
      templates: [
        { title: 'Test template 1', content: 'Test 1' },
        { title: 'Test template 2', content: 'Test 2' }
      ],
      content_css: [
        '//fonts.googleapis.com/css?family=Lato:300,300i,400,400i',
        '//www.tinymce.com/css/codepen.min.css'
      ],
      language: 'ja'
    });
}

if (typeof tinymce === "undefined") {
    // turbolinks 対策
    setTimeout(tinymce_init, 1000);
} else {
    tinymce_init();
}
