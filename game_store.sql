-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 08, 2023 at 06:59 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `game_store`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `username` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `email` varchar(25) NOT NULL,
  `password` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`username`, `name`, `phone`, `email`, `password`) VALUES
('andy', 'anderseon jum', '123434565', 'anderson@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `username` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `phone` int(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `location` varchar(100) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`username`, `name`, `phone`, `email`, `location`, `password`) VALUES
('noxx', 'Lennox Kulecho', 111368315, 'lkulecho2001@gmail.com', 'ruiru', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `games`
--

CREATE TABLE `games` (
  `product_id` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `image` varchar(50) NOT NULL,
  `cost` int(50) NOT NULL,
  `stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `games`
--

INSERT INTO `games` (`product_id`, `name`, `image`, `cost`, `stock`) VALUES
('G1', 'call of duty: black ops', 'game1.jpg', 500, 16),
('G10', 'GTA V', 'game13.jpg', 400, 11),
('G11', 'Doom: eternal', 'Game14.jpg', 400, 20),
('G12', 'Mortal kombart XL', 'game15.jpg', 400, 5),
('G2', 'Injustice: gods among us', 'game3.jpg', 250, 6),
('G3', 'Forza horizon 3', 'game2.jpg', 400, 10),
('G4', 'Fifa 20', 'game5.png', 250, 10),
('G5', 'Euro truck simulator 2', 'game7.jpg', 300, 18),
('G6', 'Need for speed: payback', 'game8.jpg', 400, 4),
('G7', 'Asphalt 8', 'game9.jpg', 300, 5),
('G8', 'Uncharted 4', 'game10.jpeg', 300, 11),
('G9', 'The last of us', 'game12.jpg', 500, 15);

-- --------------------------------------------------------

--
-- Table structure for table `new_arrivals`
--

CREATE TABLE `new_arrivals` (
  `auto_number` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `price` int(10) NOT NULL,
  `picture` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `new_arrivals`
--

INSERT INTO `new_arrivals` (`auto_number`, `name`, `price`, `picture`) VALUES
(1, 'God of war', 5000, 'god of war.jpg'),
(2, 'NFS heat', 2500, 'nfs heat.jpg'),
(3, 'Watch dogs: legion', 4500, 'watch dogs.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` varchar(10) NOT NULL,
  `product_id` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `cost` int(10) NOT NULL,
  `quantity` int(10) NOT NULL,
  `total` int(10) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `status` varchar(15) NOT NULL,
  `date/time` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `product_id`, `name`, `cost`, `quantity`, `total`, `user_name`, `status`, `date/time`) VALUES
('245ecf1a', 'G10', 'GTA V', 400, 1, 400, 'noxx', 'COMPLETE', '2023-11-08 18:34:35'),
('2cf373bd', 'T1', 'Geforce RTX', 7000, 1, 7000, 'noxx', 'COMPLETE', '2023-11-08 18:34:35'),
('474bedfa', 'G1', 'call of duty: b', 700, 1, 700, 'noxx', 'CANCELLED', '2023-11-08 18:44:03'),
('684d3203', 'T11', 'Hard disks', 1500, 2, 3000, 'noxx', 'PENDING', '2023-11-08 18:44:03'),
('llml', 'T1', 'Geforce RTX', 7000, 1, 7000, 'noxx', 'PENDING', '2023-11-08 18:36:23'),
('llmlp', 'G1', 'call of duty: b', 700, 1, 700, 'noxx', 'PENDING', '2023-11-08 18:36:56');

-- --------------------------------------------------------

--
-- Table structure for table `tech`
--

CREATE TABLE `tech` (
  `product_id` varchar(10) NOT NULL,
  `name` varchar(50) NOT NULL,
  `image` varchar(50) NOT NULL,
  `cost` int(50) NOT NULL,
  `stock` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tech`
--

INSERT INTO `tech` (`product_id`, `name`, `image`, `cost`, `stock`) VALUES
('T1', 'Geforce RTX', 'tech1.jpg', 7500, 18),
('T10', 'Gaming monitors', 'tech12.jpg', 10000, 4),
('T11', 'Hard disks', 'tech13.jpg', 1500, 5),
('T2', 'Console controllers', 'tech2.jpg', 450, 5),
('T3', 'PS4 controllers', 'tech3.jpg', 4000, 5),
('T4', 'Console chargers', 'tech4.jpg', 1500, 10),
('T5', 'HDMI cable', 'tech6.jpg', 600, 14),
('T6', 'ROG gaming pc', 'tech8.jpg', 110000, 15),
('T7', 'Gaming headphones', 'tech9.jpg', 2500, 20),
('T8', 'Wireless mice', 'tech10.jpg', 600, 5),
('T9', 'Keyboards', 'tech11.jpg', 500, 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `games`
--
ALTER TABLE `games`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `new_arrivals`
--
ALTER TABLE `new_arrivals`
  ADD PRIMARY KEY (`auto_number`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`);

--
-- Indexes for table `tech`
--
ALTER TABLE `tech`
  ADD PRIMARY KEY (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `new_arrivals`
--
ALTER TABLE `new_arrivals`
  MODIFY `auto_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
