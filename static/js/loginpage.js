const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.regiter-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', ()=>{
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=>{
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=>{
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=>{
    wrapper.classList.remove('active-popup');
});



// ------------------------------------------
// // Form submission logic
// document.querySelector('.form-box.login form').addEventListener('submit', async function (e) {
//     e.preventDefault(); // Prevent the default form submission

//     const email = document.querySelector('.form-box.login input[type="email"]').value;
//     const password = document.querySelector('.form-box.login input[type="password"]').value;

//     try {
//         const response = await fetch('http://127.0.0.1:5000/login', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ username: email, password: password }),
//         });

//         const data = await response.json();

//         if (response.ok) {
//             alert(`Login successful!`);
//             // Save the JWT token to localStorage
//             localStorage.setItem('token', data.access_token);
//         } else {
//             alert(`Error: ${data.message}`);
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred while logging in.');
//     }
// });

// document.querySelector('.form-box.register form').addEventListener('submit', async function (e) {
//     e.preventDefault(); // Prevent the default form submission

//     const username = document.querySelector('.form-box.register input[type="text"]').value;
//     const email = document.querySelector('.form-box.register input[type="email"]').value;
//     const password = document.querySelector('.form-box.register input[type="password"]').value;

//     try {
//         const response = await fetch('http://127.0.0.1:5000/register', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ username: email, password: password }),
//         });

//         const data = await response.json();

//         if (response.ok) {
//             alert('Registration successful!');
//             // Switch to login form after successful registration
//             document.querySelector('.login-link').click();
//         } else {
//             alert(`Error: ${data.message}`);
//         }
//     } catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred during registration.');
//     }
// });





// ///////////////////////////////////////////////////////////////////////////
document.querySelector('.form-box.login form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent the default form submission

    const email = document.querySelector('.form-box.login input[type="email"]').value;
    const password = document.querySelector('.form-box.login input[type="password"]').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: email, password: password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Login successful, save the JWT token
            localStorage.setItem('token', data.access_token);

            // Redirect to the next page (e.g., dashboard.html)
            window.location.href = '/dashboard';
        } else {
            // Show an error message
            alert(`Login failed: ${data.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while logging in.');
    }
});

