document.getElementById('generateBtn1').addEventListener('click', async () => {
    const fileInput = document.getElementById('txtFile');
    const delimiterInput = document.getElementById('delimiter');
    const file = fileInput.files[0];
    const delimiter = delimiterInput.value || '，'; // Default to '，' if no input

    if (!file) {
        alert('Please upload a TXT file.');
        return;
    }

    const formData = new FormData();
    formData.append('txtFile', file);
    formData.append('delimiter', delimiter); // Add delimiter to form data

    try {
        const response = await fetch('/generate-xml', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.text();
            document.getElementById('xmlContent').textContent = data;

            // Create a Blob for the generated XML
            const blob = new Blob([data], { type: 'application/xml' });
            const url = URL.createObjectURL(blob);

            // Remove old download links if any
            const oldLink = document.querySelector('#xmlOutput a');
            if (oldLink) oldLink.remove();

            // Create a link for downloading
            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = 'generated.xml';
            downloadLink.textContent = 'Download XML File';

            // Revoke the Blob URL after download
            downloadLink.addEventListener('click', () => {
                setTimeout(() => URL.revokeObjectURL(url), 1000);
            });

            document.getElementById('xmlOutput').appendChild(downloadLink);
        } else {
            const errorText = await response.text();
            alert(`Error generating XML: ${errorText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while generating XML.');
    }
});

document.getElementById('generateBtn2').addEventListener('click', async () => {
    const fileInput = document.getElementById('txtFile2');
    const delimiterInput = document.getElementById('delimiter2');
    const file = fileInput.files[0];
    const delimiter = delimiterInput.value || '，';

    if (!file) {
        alert('Please upload a TXT file.');
        return;
    }

    const formData = new FormData();
    formData.append('txtFile2', file);
    formData.append('delimiter2', delimiter);

    try {
        const response = await fetch('/generate-xml', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.text();
            document.getElementById('xmlContent').textContent = data;
            
            // Create a Blob for the generated XML
            const blob = new Blob([data], { type: 'application/xml' });
            const url = URL.createObjectURL(blob);

            // Remove old download links if any
            const oldLink = document.querySelector('#xmlOutput a');
            if (oldLink) oldLink.remove();

            // Create a link for downloading
            const downloadLink = document.createElement('a');
            downloadLink.href = url;
            downloadLink.download = 'generated.xml';
            downloadLink.textContent = 'Download XML File';

            // Revoke the Blob URL after download
            downloadLink.addEventListener('click', () => {
                setTimeout(() => URL.revokeObjectURL(url), 1000);
            });

            document.getElementById('xmlOutput').appendChild(downloadLink);
        } else {
            const errorText = await response.text();
            alert(`Error generating XML: ${errorText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while generating XML.');
    }
});