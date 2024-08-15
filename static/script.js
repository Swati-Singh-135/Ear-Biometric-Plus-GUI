function showInstructions() {
    Swal.fire({
      title: 'Instructions',
      html: `
      <b>Instructions:</b>
      <br>
      To ensure that the ear image is clear and suitable for generating a high-quality feature vector, follow these tips:
      <ul>
        <li>Remove any earrings or other ornaments from the ear before taking the image.</li>
        <li>Position the camera directly perpendicular to the ear to avoid any distortion or skew.</li>
        <li>Make sure the room is well-lit to minimize any shadows or glare on the ear.</li>
        <li>Remember that all fields are required to be filled out, so double-check your information before submitting.</li>
        <li>Verify that all the fields are filled correctly, check the spelling and accuracy of all the information before submitting the form.</li>
        <li>Make sure that the image is in focus and not blurry or pixelated.</li>
        <li>If possible, use a high-resolution camera to capture the image.</li>
        <li>Avoid any reflections or glare on the image.</li>
        <li>Ensure that the ear is centered in the frame and take the photo in a well-lit and neutral background.</li>
      </ul>
      `,
      icon: 'info',
      confirmButtonText: 'Got it',
      width: '90vw'
    })
  }


